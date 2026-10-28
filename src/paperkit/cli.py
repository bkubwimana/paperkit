"""pk: the paperkit command line."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from paperkit import REPO_URL, __version__
from paperkit import install as kit
from paperkit import status as st

TOOLS = [
    # name, candidates, required, purpose
    ("git", ["git"], True, "version control, install records"),
    ("bash", ["bash"], True, "phase scripts called by the agents"),
    ("python", ["python3", "python"], True, "text scanner"),
    ("latexmk", ["latexmk"], False, "building the paper"),
    ("tex engine", ["pdflatex", "lualatex", "xelatex"], False, "building the paper"),
    ("uv", ["uv"], False, "pk self upgrade"),
    ("claude", ["claude"], False, "Claude Code agent"),
    ("codex", ["codex"], False, "Codex agent"),
]


def _agents_arg(value: str) -> list[str]:
    if value.strip().lower() in ("none", ""):
        return []
    agents = [a.strip().lower() for a in value.split(",") if a.strip()]
    for a in agents:
        if a not in kit.AGENT_SKILL_DIRS:
            raise argparse.ArgumentTypeError(
                f"unknown agent '{a}' (choose from {', '.join(kit.AGENT_SKILL_DIRS)}, or none)")
    return sorted(set(agents))


def _root(args) -> Path:
    return kit.require_root(Path(args.dir) if getattr(args, "dir", None) else None)


# ---------------------------------------------------------------- commands

def cmd_init(args) -> int:
    if args.here or args.project in (None, "."):
        target = Path.cwd()
    else:
        target = Path(args.project)
    root = kit.init(target, agents=args.ai, venue=args.venue, no_git=args.no_git, force=args.force)
    print()
    print("Next:")
    print(f"  1. Read {kit.GUIDELINES} and adjust it to this project.")
    step = "/paper-venue" + (f" {args.venue.upper()} <year>" if args.venue else " <venue> <year>")
    print(f"  2. In your agent, run {step}.")
    print("  3. Run `pk status` any time to see what is done and what is next.")
    if root != Path.cwd().resolve():
        print(f"\n  cd {root}")
    return 0


def cmd_upgrade(args) -> int:
    rep = kit.upgrade(_root(args), dry_run=args.dry_run, force=args.force)
    if rep.counts.get("keep edited"):
        print(f"\nReview each *{kit.NEW_SUFFIX} file, merge what you want, then delete it.")
    return 0


def cmd_uninstall(args) -> int:
    root = _root(args)
    if not args.yes:
        print(f"This removes paperkit from {root}. Edited kit files and paper/ are kept.")
        print("Re-run with --yes to proceed.")
        return 1
    kit.uninstall(root)
    return 0


def cmd_status(args) -> int:
    rep = st.collect(_root(args))
    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print(st.render(rep))
    return 0


def cmd_scan(args) -> int:
    root = _root(args)
    script = root / kit.KIT_DIR / "scripts" / "bash" / "scan_text.py"
    if not script.is_file():
        print(f"scanner missing at {script}; run `pk upgrade`", file=sys.stderr)
        return 2
    cmd = [sys.executable, "-I", str(script), str(args.path or root), "--ext", args.ext]
    return subprocess.run(cmd, check=False).returncode


def cmd_check(args) -> int:
    missing_required = False
    print(f"{'tool':<12} {'status':<9} purpose")
    for name, candidates, required, purpose in TOOLS:
        found = next((c for c in candidates if shutil.which(c)), None)
        if found:
            state = "ok"
        elif required:
            state = "MISSING"
            missing_required = True
        else:
            state = "absent"
        print(f"{name:<12} {state:<9} {purpose}")
    root = kit.find_root()
    if root:
        print(f"\nproject: {root}")
        cfg = kit.load_config(root)
        print(f"  kit {cfg.get('kit_version', '?')}, agents {', '.join(cfg.get('agents', [])) or 'none'}")
    if missing_required:
        print("\nRequired tools are missing.")
        return 1
    print("\nAll required tools present.")
    return 0


def cmd_version(args) -> int:
    info = {
        "pk": kit.kit_version_string(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "install_commit": kit.install_commit(),
    }
    root = kit.find_root()
    if root:
        cfg = kit.load_config(root)
        info["project"] = str(root)
        info["project_kit_version"] = cfg.get("kit_version")
    if args.json:
        print(json.dumps(info, indent=2))
    else:
        for k, v in info.items():
            print(f"{k:<20} {v}")
    return 0


def cmd_venue(args) -> int:
    assets = kit.Assets()
    if args.venue_cmd == "list":
        root = kit.find_root()
        current = kit.load_config(root).get("venue") if root else None
        for name, path in assets.venues().items():
            lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
            title = lines[0].lstrip("# ") if lines else name
            blurb = lines[1].split(".")[0] if len(lines) > 1 else ""
            mark = "*" if name == current else " "
            print(f"{mark} {name:<11} {title}: {blurb}")
        return 0
    if args.venue_cmd == "info":
        venues = assets.venues()
        if args.name not in venues:
            print(f"unknown venue '{args.name}'. Known: {', '.join(venues)}", file=sys.stderr)
            return 1
        print(venues[args.name].read_text(encoding="utf-8"))
        return 0
    if args.venue_cmd == "use":
        root = _root(args)
        kit.set_venue(root, args.name)
        print(f"default venue for {root}: {args.name}")
        return 0
    return 2


def cmd_agent(args) -> int:
    if args.agent_cmd == "list":
        root = kit.find_root()
        installed = kit.load_config(root).get("agents", []) if root else []
        for name, d in kit.AGENT_SKILL_DIRS.items():
            mark = "installed" if name in installed else ""
            print(f"{name:<8} {d:<16} context {kit.AGENT_CONTEXT[name]:<10} {mark}")
        return 0
    root = _root(args)
    agents = set(kit.load_config(root).get("agents", []))
    if args.agent_cmd == "add":
        agents.add(args.name)
    elif args.agent_cmd == "remove":
        agents.discard(args.name)
    kit.set_agents(root, sorted(agents))
    print(f"agents: {', '.join(sorted(agents)) or 'none'}")
    return 0


def cmd_self(args) -> int:
    installed = kit.install_commit()
    remote = None
    try:
        out = subprocess.run(["git", "ls-remote", REPO_URL, "HEAD"], capture_output=True,
                             text=True, timeout=60, check=False,
                             env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        if out.returncode == 0 and out.stdout:
            remote = out.stdout.split()[0]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    if args.self_cmd == "check":
        print(f"installed: {kit.kit_version_string()}")
        print(f"latest:    {remote[:7] if remote else 'unknown (could not reach GitHub)'}")
        if installed and remote:
            print("up to date" if installed == remote else "update available: pk self upgrade")
        elif not installed:
            print("not installed from git (dev checkout?); compare manually")
        return 0
    if args.self_cmd == "upgrade":
        if args.dry_run:
            print(f"would upgrade {kit.kit_version_string()} to {remote[:7] if remote else 'latest'}")
            return 0
        uv = shutil.which("uv")
        if not uv:
            print(f"uv not found. Reinstall with: pip install --upgrade git+{REPO_URL}")
            return 1
        return subprocess.run([uv, "tool", "upgrade", "paperkit"], check=False).returncode
    return 2


# ---------------------------------------------------------------- parser

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pk",
        description="paperkit: conference grounding for agent-assisted paper writing.",
        epilog="Phases run inside your agent: /paper-venue, /paper-claims, /paper-outline, "
               "/paper-figures, /paper-review, /paper-check.",
    )
    p.add_argument("-V", "--version", action="version", version=f"pk {kit.kit_version_string()}")
    sub = p.add_subparsers(dest="cmd", metavar="COMMAND")

    s = sub.add_parser("init", help="set up paperkit in a paper repository")
    s.add_argument("project", nargs="?", help="directory to set up (created if missing); '.' for here")
    s.add_argument("--here", action="store_true", help="set up in the current directory")
    s.add_argument("--venue", help="default target venue (see `pk venue list`)")
    s.add_argument("--ai", type=_agents_arg, default=["claude"],
                   help="agents to install commands for: claude, codex, both as claude,codex, or none "
                        "(default: claude)")
    s.add_argument("--no-git", action="store_true", help="do not run git init")
    s.add_argument("--force", action="store_true", help="re-initialize, overwriting edited kit files")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("upgrade", help="update the kit in this project, keeping your edits")
    s.add_argument("--dir", help="project directory (default: search upward from here)")
    s.add_argument("--dry-run", action="store_true", help="show what would change")
    s.add_argument("--force", action="store_true", help="overwrite edited kit files")
    s.set_defaults(func=cmd_upgrade)

    s = sub.add_parser("uninstall", help="remove the kit, keeping edited files and paper/")
    s.add_argument("--dir")
    s.add_argument("--yes", action="store_true", help="confirm")
    s.set_defaults(func=cmd_uninstall)

    s = sub.add_parser("status", help="show phase progress, claim status and blockers")
    s.add_argument("--dir")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("scan", help="flag placeholders and banned terms in the paper source")
    s.add_argument("path", nargs="?", help="directory to scan (default: project root)")
    s.add_argument("--dir")
    s.add_argument("--ext", default=".tex", help="comma-separated extensions (default .tex)")
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("check", help="check required tools are installed")
    s.set_defaults(func=cmd_check)

    s = sub.add_parser("version", help="show version and system information")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_version)

    s = sub.add_parser("venue", help="list, inspect or select venue profiles")
    vs = s.add_subparsers(dest="venue_cmd", metavar="ACTION", required=True)
    vs.add_parser("list", help="list bundled venue profiles")
    v = vs.add_parser("info", help="print a venue profile")
    v.add_argument("name")
    v = vs.add_parser("use", help="set this project's default venue")
    v.add_argument("name")
    v.add_argument("--dir")
    s.set_defaults(func=cmd_venue)

    s = sub.add_parser("agent", help="manage which agents get the phase commands")
    ag = s.add_subparsers(dest="agent_cmd", metavar="ACTION", required=True)
    ag.add_parser("list", help="list supported agents")
    for action in ("add", "remove"):
        a = ag.add_parser(action, help=f"{action} an agent")
        a.add_argument("name", choices=sorted(kit.AGENT_SKILL_DIRS))
        a.add_argument("--dir")
    s.set_defaults(func=cmd_agent)

    s = sub.add_parser("self", help="check for or install a newer pk")
    ss = s.add_subparsers(dest="self_cmd", metavar="ACTION", required=True)
    ss.add_parser("check", help="compare the installed pk with the latest on GitHub")
    u = ss.add_parser("upgrade", help="upgrade pk with uv")
    u.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_self)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except kit.KitError as exc:
        print(f"pk: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
