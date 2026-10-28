"""Read the paper/ artifacts and summarize how far the paper is from submittable."""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from paperkit.install import CONFIG, NEW_SUFFIX, load_json

CLAIM_STATUSES = ("M", "D", "E", "U", "C")
FIGURE_STATUSES = ("planned", "drafted", "final")
SEVERITIES = ("reject", "major", "minor")
PHASES = [
    ("venue", "paper/venue.md", "/paper-venue"),
    ("claims", "paper/claims.md", "/paper-claims"),
    ("outline", "paper/outline.md", "/paper-outline"),
    ("figures", "paper/figures.md", "/paper-figures"),
]
_SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def tables(text: str):
    """Yield (header, rows) for each pipe table in markdown text."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and _SEP.match(lines[i + 1]):
            header = [h.lower() for h in _cells(lines[i])]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(_cells(lines[j]))
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def _col(header: list[str], name: str) -> int | None:
    return header.index(name) if name in header else None


def parse_claims(text: str) -> dict:
    out = {"headline": {s: 0 for s in CLAIM_STATUSES}, "supporting": {s: 0 for s in CLAIM_STATUSES},
           "unset": 0, "blockers": []}
    for header, rows in tables(text):
        i_id, i_st = _col(header, "id"), _col(header, "status")
        if i_id is None or i_st is None:
            continue
        for row in rows:
            if max(i_id, i_st) >= len(row):
                continue
            cid, st = row[i_id], row[i_st].strip().upper()
            if not re.match(r"^[HS]\d+", cid):
                continue
            if st not in CLAIM_STATUSES:
                out["unset"] += 1
                continue
            kind = "headline" if cid.startswith("H") else "supporting"
            out[kind][st] += 1
            if kind == "headline" and st in ("E", "U"):
                out["blockers"].append(f"{cid} is a headline claim with status {st}")
    return out


def parse_figures(text: str) -> dict:
    out = {s: 0 for s in FIGURE_STATUSES}
    out["other"] = 0
    for header, rows in tables(text):
        i_id, i_st = _col(header, "id"), _col(header, "status")
        if i_id is None or i_st is None:
            continue
        for row in rows:
            if max(i_id, i_st) >= len(row) or not re.match(r"^[FT]\d+", row[i_id]):
                continue
            st = row[i_st].strip().lower()
            out[st if st in FIGURE_STATUSES else "other"] += 1
    return out


def parse_venue(text: str, today: _dt.date) -> dict:
    out = {"name": None, "deadline": None, "days_left": None, "unverified": 0}
    m = re.search(r"^#\s*Target venue:\s*(.+)$", text, re.M)
    if m and "[" not in m.group(1):
        out["name"] = m.group(1).strip()
    for header, rows in tables(text):
        for row in rows:
            if any("UNVERIFIED" in c for c in row):
                out["unverified"] += 1
            if row and row[0].strip().lower() == "deadline" and len(row) > 1:
                d = _DATE.search(row[1])
                if d:
                    date = _dt.date(int(d.group(1)), int(d.group(2)), int(d.group(3)))
                    out["deadline"] = date.isoformat()
                    out["days_left"] = (date - today).days
    return out


def parse_review(text: str) -> dict:
    out = {s: 0 for s in SEVERITIES}
    for header, rows in tables(text):
        i_sev = _col(header, "severity")
        if i_sev is None:
            continue
        for row in rows:
            if i_sev < len(row) and row[i_sev].strip().lower() in SEVERITIES:
                out[row[i_sev].strip().lower()] += 1
    return out


def parse_check(text: str) -> str | None:
    m = re.search(r"^##\s*Result\s*$(.*)", text, re.M | re.S)
    if not m:
        return None
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("PASS"):
            return "PASS"
        if line.startswith("FAIL"):
            return "FAIL"
    return None


def collect(root: Path, today: _dt.date | None = None) -> dict:
    today = today or _dt.date.today()
    config = load_json(root / CONFIG, {})
    paper = root / "paper"
    rep: dict = {
        "root": str(root),
        "kit_version": config.get("kit_version"),
        "agents": config.get("agents", []),
        "venue_default": config.get("venue"),
        "phases": {},
        "blockers": [],
        "next": None,
    }

    def read(rel: str) -> str | None:
        p = root / rel
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

    for name, rel, _cmd in PHASES:
        rep["phases"][name] = {"file": rel, "exists": (root / rel).is_file()}

    venue = read("paper/venue.md")
    if venue is not None:
        v = parse_venue(venue, today)
        rep["phases"]["venue"].update(v)
        if v["unverified"]:
            rep["blockers"].append(f"{v['unverified']} venue constraint(s) UNVERIFIED")
        if v["days_left"] is not None and v["days_left"] < 0:
            rep["blockers"].append(f"deadline {v['deadline']} has passed")

    claims = read("paper/claims.md")
    if claims is not None:
        c = parse_claims(claims)
        rep["phases"]["claims"].update(c)
        rep["blockers"].extend(c["blockers"])

    figures = read("paper/figures.md")
    if figures is not None:
        rep["phases"]["figures"].update(parse_figures(figures))

    reviews = sorted(paper.glob("review-*.md")) if paper.is_dir() else []
    rep["phases"]["review"] = {"exists": bool(reviews), "file": reviews[-1].relative_to(root).as_posix() if reviews else None}
    if reviews:
        r = parse_review(reviews[-1].read_text(encoding="utf-8", errors="replace"))
        rep["phases"]["review"].update(r)
        if r["reject"]:
            rep["blockers"].append(f"{r['reject']} reject-level finding(s) in {reviews[-1].name}")

    check = read("paper/submission-check.md")
    rep["phases"]["check"] = {"exists": check is not None, "file": "paper/submission-check.md",
                              "result": parse_check(check) if check else None}

    tbd = 0
    if paper.is_dir():
        for p in paper.glob("*.md"):
            tbd += len(re.findall(r"\bTBD\b", p.read_text(encoding="utf-8", errors="replace")))
    rep["tbd"] = tbd
    rep["pending_new_versions"] = sorted(
        p.relative_to(root).as_posix() for p in root.rglob(f"*{NEW_SUFFIX}") if ".git" not in p.parts
    )

    for name, _rel, cmd in PHASES:
        if not rep["phases"][name]["exists"]:
            rep["next"] = cmd
            break
    else:
        if any("headline claim" in b for b in rep["blockers"]):
            rep["next"] = "/paper-claims"
        elif not reviews:
            rep["next"] = "/paper-review"
        elif check is None:
            rep["next"] = "/paper-check"
        elif rep["phases"]["check"]["result"] != "PASS":
            rep["next"] = "fix the failing items, then /paper-check"
        else:
            rep["next"] = "submit"
    return rep


def render(rep: dict) -> str:
    out: list[str] = []
    venue = rep["phases"]["venue"]
    head = f"paperkit {rep['kit_version'] or '?'}  agents: {', '.join(rep['agents']) or 'none'}"
    vname = venue.get("name") or rep["venue_default"]
    if vname:
        head += f"  venue: {vname}"
    out.append(head)
    if venue.get("deadline"):
        out.append(f"deadline {venue['deadline']} ({venue['days_left']} days)")
    out.append("")

    def box(ok: bool) -> str:
        return "[x]" if ok else "[ ]"

    v = rep["phases"]["venue"]
    out.append(f"{box(v['exists'])} venue    " + (f"{v.get('unverified', 0)} unverified constraint(s)" if v["exists"] else ""))
    c = rep["phases"]["claims"]
    if c["exists"]:
        def fmt(d):
            parts = [f"{k}{d[k]}" for k in CLAIM_STATUSES if d[k]]
            return " ".join(parts) or "none"
        out.append(f"[x] claims   headline {fmt(c['headline'])} | supporting {fmt(c['supporting'])}"
                   + (f" | {c['unset']} without status" if c["unset"] else ""))
    else:
        out.append("[ ] claims")
    o = rep["phases"]["outline"]
    out.append(f"{box(o['exists'])} outline")
    f = rep["phases"]["figures"]
    if f["exists"]:
        out.append(f"[x] figures  final {f['final']} | drafted {f['drafted']} | planned {f['planned']}")
    else:
        out.append("[ ] figures")
    r = rep["phases"]["review"]
    if r["exists"]:
        out.append(f"[x] review   {r['file']}: reject {r['reject']} | major {r['major']} | minor {r['minor']}")
    else:
        out.append("[ ] review")
    k = rep["phases"]["check"]
    out.append(f"{box(k['exists'])} check    " + (k["result"] or ("no result" if k["exists"] else "")))
    out.append("")
    out.append(f"TBD in paper/: {rep['tbd']}")
    if rep["pending_new_versions"]:
        out.append(f"kit files awaiting review ({NEW_SUFFIX}): {len(rep['pending_new_versions'])}")
        out.extend(f"  {p}" for p in rep["pending_new_versions"])
    if rep["blockers"]:
        out.append("blockers:")
        out.extend(f"  - {b}" for b in rep["blockers"])
    out.append(f"next: {rep['next']}")
    return "\n".join(line.rstrip() for line in out)
