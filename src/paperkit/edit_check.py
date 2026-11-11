"""Conservative protected-token comparison for an editorial pass.

This is not a TeX parser or a scientific-equivalence check. Counts catch added,
removed and duplicated tokens, but cannot bind a result to its original subject.
"""
from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path

_COMMAND = re.compile(
    r"\\(?P<name>[A-Za-z]+)\*?\s*(?:\[[^\]]*\]\s*)*\{(?P<body>[^{}]*)\}"
)
_MATH = re.compile(
    r"(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$"
    r"|\\\[.*?\\\]|\\\(.*?\\\)"
    r"|\\begin\{(?P<env>equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|displaymath|math)\}"
    r".*?\\end\{(?P=env)\}",
    re.S,
)
_NUMBER_BODY = r"[-+]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?"
_NUMBER = re.compile(r"(?<![\w.])" + _NUMBER_BODY + r"(?!\w|\.\d)")
_QUANTITY = re.compile(
    r"(?<![\w.])" + _NUMBER_BODY
    + r"(?:\s|~|\\[,;! ])*"
    + r"(?:\\%|%|[kMGT]?Hz|[pnumkMGTµμ]?[sWJ]|[kKMGT]?[bB](?:/s)?|[KMGT]iB(?:/s)?"
    r"|cycles?|cores?|threads?|lanes?|entries|instructions?|accesses|bytes?)(?!\w)"
)
_QUALIFIERS = re.compile(
    r"\b(?:measured|modelled|modeled|estimated|simulated|suggests?|hypothesi[sz]e[sd]?"
    r"|may|might|median|mean|geometric mean|up to|at most|at least)\b", re.I
)
_REFERENCES = {"ref", "autoref", "cref", "Cref", "eqref", "pageref", "vref", "Vref"}
_PATHS = {"input", "include", "includegraphics", "url", "href"}


def strip_tex_comments(text: str) -> str:
    """Remove unescaped % comments, respecting even/odd backslash counts."""
    out = []
    for line in text.splitlines(keepends=True):
        for i, char in enumerate(line):
            if char != "%":
                continue
            j = i - 1
            while j >= 0 and line[j] == "\\":
                j -= 1
            if (i - j - 1) % 2 == 0:
                line = line[:i] + ("\n" if line.endswith("\n") else "")
                break
        out.append(line)
    return "".join(out)


def inventory(text: str, *, latex: bool = True, terms: tuple[str, ...] = ()) -> dict:
    text = strip_tex_comments(text) if latex else text
    groups: dict[str, Counter] = {
        key: Counter() for key in
        ("numbers", "quantities", "citations", "references", "labels", "math",
         "paths", "qualifiers", "terms")
    }
    # Exclude digits inside citation/label/path identifiers from prose numbers.
    # A changed key is reported in its own category, not as a numerical result.
    def command(match):
        name, body = match.group("name", "body")
        if name.lower().startswith("cite") or name in {"nocite", "parencite", "textcite",
                                                           "autocite", "footcite", "smartcite",
                                                           "Textcite", "Parencite"}:
            group = "citations"
        elif name in _REFERENCES:
            group = "references"
        elif name == "label":
            group = "labels"
        elif name in _PATHS:
            group = "paths"
        else:
            return match.group(0)
        keys = body.split(",") if group in {"citations", "references"} else [body]
        groups[group].update(key.strip() for key in keys if key.strip())
        # Keep optional arguments visible: e.g. a changed citation page number
        # or includegraphics width should still count as a numerical edit.
        prefix = match.group(0)[:match.start("body") - match.start()]
        return prefix + " " * len(body) + "}"

    prose = _COMMAND.sub(command, text) if latex else text
    groups["numbers"].update(_NUMBER.findall(prose))
    groups["quantities"].update(
        re.sub(r"\s+|~|\\[,;! ]", "", m.group(0)) for m in _QUANTITY.finditer(prose)
    )
    if latex:
        groups["math"].update(" ".join(m.group(0).split()) for m in _MATH.finditer(text))
    groups["qualifiers"].update(m.group(0).lower() for m in _QUALIFIERS.finditer(prose))
    for term in terms:
        if not term.strip():
            continue
        pattern = r"(?<!\w)" + r"\s+".join(re.escape(t) for t in term.split()) + r"(?!\w)"
        groups["terms"][term] = len(re.findall(pattern, prose))
    return groups


def compare(before: str, after: str, *, latex: bool = True, terms: tuple[str, ...] = ()) -> dict:
    old, new = inventory(before, latex=latex, terms=terms), inventory(after, latex=latex, terms=terms)
    changes = {}
    for category in old:
        removed, added = old[category] - new[category], new[category] - old[category]
        if removed or added:
            changes[category] = {
                direction: [{"value": v, "count": n} for v, n in sorted(counts.items())]
                for direction, counts in (("removed", removed), ("added", added))
            }
    return {"result": "REVIEW" if changes else "PASS", "changes": changes,
            "limitation": "Protected-token comparison only. Manually review scientific meaning, "
                          "number-to-result associations, evidence status, negation and scope; "
                          "custom TeX macros and included files are not expanded."}


def check_files(before: Path, after: Path, *, terms: tuple[str, ...] = ()) -> dict:
    if before.resolve() == after.resolve():
        raise ValueError("before and after must be different files; keep an original baseline")
    if before.suffix.lower() != after.suffix.lower() or before.suffix.lower() not in {".tex", ".md"}:
        raise ValueError("compare two .tex files or two .md files")
    raw_before, raw_after = before.read_bytes(), after.read_bytes()
    rep = compare(raw_before.decode("utf-8-sig"), raw_after.decode("utf-8-sig"),
                  latex=before.suffix.lower() == ".tex", terms=terms)
    rep["before"] = {"path": str(before), "sha256": hashlib.sha256(raw_before).hexdigest()}
    rep["after"] = {"path": str(after), "sha256": hashlib.sha256(raw_after).hexdigest()}
    return rep


def render(rep: dict) -> str:
    out = [f"{rep['result']}: editorial preservation check"]
    for category, change in rep["changes"].items():
        out.append(f"  {category}:")
        for direction in ("removed", "added"):
            out.extend(f"    {direction} {item['count']} x {item['value']}" for item in change[direction])
    for version in ("before", "after"):
        out.append(f"{version}: {rep[version]['path']}  sha256={rep[version]['sha256']}")
    out.append(rep["limitation"])
    return "\n".join(out)
