"""Install, upgrade and uninstall the kit in a paper repository.

Every file the kit writes is recorded in .paperkit/manifest.json with its
SHA-256. Upgrades replace a file only while it still matches the recorded
hash; a file the user edited is kept and the new version is written beside it
as <file>.paperkit-new. Uninstall removes only unmodified files.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from paperkit import __version__

KIT_DIR = ".paperkit"
MANIFEST = f"{KIT_DIR}/manifest.json"
CONFIG = f"{KIT_DIR}/config.json"
NEW_SUFFIX = ".paperkit-new"

AGENT_SKILL_DIRS = {
    "claude": ".claude/skills",
    "codex": ".agents/skills",
}
AGENT_CONTEXT = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
}
POINTER_MARKER = "paperkit: read .paperkit/AGENTS.md"
AGENTS_POINTER = (
    "Paper writing in this repository follows paperkit. Read "
    "`.paperkit/AGENTS.md` before editing any paper text, figure or number."
)
CLAUDE_POINTER = "@.paperkit/AGENTS.md"
LEGACY_GUIDELINES = f"{KIT_DIR}/memory/constitution.md"
GUIDELINES = f"{KIT_DIR}/memory/guidelines.md"


class KitError(Exception):
    """A problem the user must resolve; printed without a traceback."""


# ---------------------------------------------------------------- assets

class Assets:
    """Locate the bundled kit: inside the wheel, or the repo for dev runs."""

    def __init__(self) -> None:
        pkg = Path(__file__).resolve().parent / "assets"
        if (pkg / "kit").is_dir():
            self.kit = pkg / "kit"
            self.skills = pkg / "skills"
            self.agents_md = pkg / "AGENTS.md"
        else:
            repo = Path(__file__).resolve().parents[2]
            self.kit = repo / KIT_DIR
            self.skills = repo / "skills"
            self.agents_md = repo / "AGENTS.md"
        if not self.kit.is_dir() or not self.skills.is_dir():
            raise KitError(f"kit assets not found near {pkg}")

    def venues(self) -> dict[str, Path]:
        return {
            p.stem: p
            for p in sorted((self.kit / "venues").glob("*.md"))
            if not p.stem.startswith("_")
        }

    def skill_names(self) -> list[str]:
        return sorted(d.name for d in self.skills.iterdir() if (d / "SKILL.md").is_file())


def _skip(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix == ".pyc" or path.name.endswith(NEW_SUFFIX)


def planned_files(assets: Assets, agents: list[str]) -> dict[str, Path]:
    """Map target-relative POSIX path -> source file for everything the kit owns."""
    plan: dict[str, Path] = {}
    for src in sorted(assets.kit.rglob("*")):
        if src.is_file() and not _skip(src):
            rel = src.relative_to(assets.kit).as_posix()
            if rel in ("manifest.json", "config.json", "VERSION"):
                continue
            plan[f"{KIT_DIR}/{rel}"] = src
    plan[f"{KIT_DIR}/AGENTS.md"] = assets.agents_md
    for agent in agents:
        base = AGENT_SKILL_DIRS[agent]
        for name in assets.skill_names():
            plan[f"{base}/{name}/SKILL.md"] = assets.skills / name / "SKILL.md"
    return plan


# ---------------------------------------------------------------- helpers

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def find_root(start: Path | None = None) -> Path | None:
    """Directory containing .paperkit/, searching upward."""
    d = (start or Path.cwd()).resolve()
    for cand in [d, *d.parents]:
        if (cand / KIT_DIR).is_dir():
            return cand
    return None


def require_root(start: Path | None = None) -> Path:
    root = find_root(start)
    if root is None:
        raise KitError("not inside a paperkit project (no .paperkit/ found). Run `pk init` first.")
    return root


def load_json(path: Path, default):
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KitError(f"{path} is not valid JSON: {exc}") from exc


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def load_config(root: Path) -> dict:
    return load_json(root / CONFIG, {})


def load_manifest(root: Path) -> dict[str, str]:
    return load_json(root / MANIFEST, {}).get("files", {})


def install_commit() -> str | None:
    """Commit the CLI was installed from, when installed from git."""
    try:
        from importlib import metadata
        raw = metadata.distribution("paperkit").read_text("direct_url.json")
        if raw:
            return json.loads(raw).get("vcs_info", {}).get("commit_id")
    except Exception:
        return None
    return None


def kit_version_string() -> str:
    commit = install_commit()
    return f"{__version__}+{commit[:7]}" if commit else __version__


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    if path.suffix in (".sh", ".py") and "/scripts/" in path.as_posix():
        mode = path.stat().st_mode
        path.chmod(mode | 0o111)


def _in_git(root: Path) -> bool:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, check=False,
        )
        return out.returncode == 0 and out.stdout.strip() == "true"
    except FileNotFoundError:
        return False


def _git_tracked(root: Path, rel: str) -> bool:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", rel],
            capture_output=True, text=True, check=False,
        )
        return out.returncode == 0
    except FileNotFoundError:
        return False


# ---------------------------------------------------------------- pointers

def _has_pointer(path: Path) -> bool:
    return path.is_file() and POINTER_MARKER in path.read_text(encoding="utf-8", errors="replace")


def add_pointer(path: Path, line: str) -> bool:
    if _has_pointer(path):
        return False
    prefix = ""
    if path.is_file() and path.stat().st_size > 0:
        prefix = "\n" if path.read_text(encoding="utf-8", errors="replace").endswith("\n") else "\n\n"
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{prefix}<!-- {POINTER_MARKER} -->\n{line}\n")
    return True


def remove_pointer(path: Path) -> bool:
    if not _has_pointer(path):
        return False
    lines = path.read_text(encoding="utf-8").split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        if POINTER_MARKER in lines[i]:
            if out and out[-1] == "":
                out.pop()
            i += 2
            continue
        out.append(lines[i])
        i += 1
    text = "\n".join(out).rstrip("\n")
    path.write_text(text + "\n" if text else "", encoding="utf-8", newline="\n")
    return True


def ensure_context(root: Path, agents: list[str], config: dict, log) -> None:
    agents_md = root / "AGENTS.md"
    had_agents = agents_md.is_file() and not _has_pointer(agents_md) and agents_md.stat().st_size > 0
    if add_pointer(agents_md, AGENTS_POINTER):
        log("pointer", "AGENTS.md")
    if "claude" in agents:
        claude_md = root / "CLAUDE.md"
        if not claude_md.exists():
            if had_agents:
                claude_md.write_text("@AGENTS.md\n", encoding="utf-8", newline="\n")
                log("created", "CLAUDE.md (imports the existing AGENTS.md)")
            config["created_claude_md"] = True
        if add_pointer(claude_md, CLAUDE_POINTER):
            log("pointer", "CLAUDE.md")


# ---------------------------------------------------------------- sync

class Report:
    def __init__(self, dry_run: bool, echo) -> None:
        self.dry_run = dry_run
        self.echo = echo
        self.counts: dict[str, int] = {}

    def __call__(self, action: str, what: str) -> None:
        self.counts[action] = self.counts.get(action, 0) + 1
        tag = f"would {action}" if self.dry_run else action
        self.echo(f"  {tag:<16} {what}")


def migrate_legacy_guidelines(root: Path, log, dry_run: bool) -> None:
    old, new = root / LEGACY_GUIDELINES, root / GUIDELINES
    if not old.is_file() or new.exists():
        return
    log("renamed", f"{LEGACY_GUIDELINES} -> {GUIDELINES}")
    if dry_run:
        return
    if _git_tracked(root, LEGACY_GUIDELINES):
        subprocess.run(["git", "-C", str(root), "mv", LEGACY_GUIDELINES, GUIDELINES], check=True)
    else:
        old.rename(new)
    text = new.read_text(encoding="utf-8")
    new.write_text(text.replace("# Paper Constitution", "# Paper Guidelines", 1), encoding="utf-8", newline="\n")


def sync(root: Path, agents: list[str], *, dry_run: bool = False, force: bool = False,
         echo=print) -> Report:
    """Bring the kit files in root up to the bundled version, safely."""
    assets = Assets()
    log = Report(dry_run, echo)
    manifest_path = root / MANIFEST
    legacy = (root / KIT_DIR).is_dir() and not manifest_path.is_file()
    if legacy:
        echo("  (no manifest: earlier install; edited files will be kept and new versions written beside them)")

    migrate_legacy_guidelines(root, log, dry_run)

    old_manifest = load_manifest(root)
    plan = planned_files(assets, agents)
    new_manifest: dict[str, str] = {}

    for rel, src in plan.items():
        dst = root / rel
        data = src.read_bytes()
        new_hash = sha256_bytes(data)
        if not dst.exists():
            log("add", rel)
            if not dry_run:
                _write(dst, data)
            new_manifest[rel] = new_hash
            continue
        cur_hash = sha256_file(dst)
        if cur_hash == new_hash:
            new_manifest[rel] = new_hash
            continue
        recorded = old_manifest.get(rel)
        if recorded is not None and cur_hash == recorded:
            log("update", rel)
            if not dry_run:
                _write(dst, data)
            new_manifest[rel] = new_hash
        elif force:
            log("overwrite", f"{rel} (edited, --force)")
            if not dry_run:
                _write(dst, data)
            new_manifest[rel] = new_hash
        else:
            log("keep edited", f"{rel} (new version: {rel}{NEW_SUFFIX})")
            if not dry_run:
                _write(dst.with_name(dst.name + NEW_SUFFIX), data)
            # Keep the old recorded hash so the file still reads as edited.
            new_manifest[rel] = recorded if recorded is not None else new_hash + ":unrecorded"

    for rel, recorded in old_manifest.items():
        if rel in plan:
            continue
        dst = root / rel
        if not dst.exists():
            continue
        if sha256_file(dst) == recorded:
            log("remove", rel)
            if not dry_run:
                dst.unlink()
                _prune_empty(dst.parent, root)
        else:
            log("orphan kept", f"{rel} (edited, no longer part of the kit)")

    if not dry_run:
        save_json(manifest_path, {"kit_version": kit_version_string(), "files": new_manifest})
        (root / "paper").mkdir(exist_ok=True)
    return log


def _prune_empty(directory: Path, root: Path) -> None:
    d = directory
    while d != root and d.is_dir() and not any(d.iterdir()):
        d.rmdir()
        d = d.parent


# ---------------------------------------------------------------- commands

def init(target: Path, *, agents: list[str], venue: str | None, no_git: bool,
         force: bool, echo=print) -> Path:
    assets = Assets()
    if venue is not None and venue not in assets.venues():
        raise KitError(f"unknown venue '{venue}'. Known: {', '.join(assets.venues())}")
    for a in agents:
        if a not in AGENT_SKILL_DIRS:
            raise KitError(f"unknown agent '{a}'. Known: {', '.join(AGENT_SKILL_DIRS)}")

    target.mkdir(parents=True, exist_ok=True)
    root = target.resolve()
    if (root / MANIFEST).is_file() and not force:
        raise KitError(f"{root} is already a paperkit project. Use `pk upgrade`, or `pk init --force`.")

    echo(f"paperkit {kit_version_string()} -> {root}")
    if not no_git and not _in_git(root):
        if shutil.which("git"):
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            echo("  git init")
        else:
            echo("  git not found; skipping git init")

    config = load_config(root)
    config.update({
        "agents": agents,
        "venue": venue if venue is not None else config.get("venue"),
        "kit_version": kit_version_string(),
        "initialized_at": config.get("initialized_at")
            or _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
    })
    sync(root, agents, force=force, echo=echo)
    ensure_context(root, agents, config, Report(False, echo))
    save_json(root / CONFIG, config)
    return root


def upgrade(root: Path, *, dry_run: bool, force: bool, echo=print) -> Report:
    config = load_config(root)
    agents = config.get("agents") or ["claude"]
    echo(f"paperkit {config.get('kit_version', 'unknown')} -> {kit_version_string()} in {root}")
    rep = sync(root, agents, dry_run=dry_run, force=force, echo=echo)
    if not dry_run:
        ensure_context(root, agents, config, Report(False, echo))
        config["kit_version"] = kit_version_string()
        config["agents"] = agents
        save_json(root / CONFIG, config)
    if not rep.counts:
        echo("  already up to date")
    return rep


def set_agents(root: Path, agents: list[str], echo=print) -> None:
    config = load_config(root)
    old = config.get("agents") or []
    config["agents"] = agents
    sync(root, agents, echo=echo)
    ensure_context(root, agents, config, Report(False, echo))
    if "claude" in old and "claude" not in agents:
        claude_md = root / "CLAUDE.md"
        if remove_pointer(claude_md):
            echo("  pointer removed  CLAUDE.md")
    save_json(root / CONFIG, config)


def uninstall(root: Path, echo=print) -> None:
    manifest = load_manifest(root)
    config = load_config(root)
    kept: list[str] = []
    for rel, recorded in sorted(manifest.items()):
        p = root / rel
        if not p.exists():
            continue
        if sha256_file(p) == recorded:
            p.unlink()
            _prune_empty(p.parent, root)
        else:
            kept.append(rel)
    for rel in [MANIFEST, CONFIG, f"{KIT_DIR}/VERSION"]:
        p = root / rel
        if p.exists():
            p.unlink()
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = root / name
        if remove_pointer(p):
            echo(f"  pointer removed  {name}")
            text = p.read_text(encoding="utf-8").strip()
            if not text or (name == "CLAUDE.md" and config.get("created_claude_md") and text == "@AGENTS.md"):
                p.unlink()
                echo(f"  removed          {name} (created by paperkit)")
    for d in (root / KIT_DIR, root / ".claude" / "skills", root / ".agents" / "skills"):
        if d.is_dir():
            for sub in sorted(d.rglob("*"), reverse=True):
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
            _prune_empty(d, root)
    echo(f"  removed {len(manifest) - len(kept)} kit files")
    for rel in kept:
        echo(f"  kept (edited)    {rel}")
    if (root / "paper").is_dir():
        echo("  kept             paper/ (your artifacts)")


def set_venue(root: Path, name: str) -> None:
    venues = {p.stem for p in (root / KIT_DIR / "venues").glob("*.md") if not p.stem.startswith("_")}
    if name not in venues:
        raise KitError(f"unknown venue '{name}'. In this project: {', '.join(sorted(venues))}")
    config = load_config(root)
    config["venue"] = name
    save_json(root / CONFIG, config)
