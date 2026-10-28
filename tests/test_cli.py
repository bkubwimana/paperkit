"""End-to-end tests for pk. Run: PYTHONPATH=src python -m unittest discover -s tests"""
from __future__ import annotations

import contextlib
import datetime as dt
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from paperkit import install as kit
from paperkit import status as st
from paperkit.cli import main


def run(*argv: str) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = main(list(argv))
    return code, buf.getvalue()


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self._cwd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def init(self, *extra: str) -> Path:
        root = self.tmp / "paper-repo"
        code, out = run("init", str(root), "--no-git", *extra)
        self.assertEqual(code, 0, out)
        os.chdir(root)
        return root


class InitTests(Base):
    def test_init_installs_kit_skills_and_pointers(self):
        root = self.init("--venue", "isca", "--ai", "claude,codex")
        self.assertTrue((root / ".paperkit/memory/guidelines.md").is_file())
        self.assertTrue((root / ".paperkit/venues/isca.md").is_file())
        self.assertTrue((root / ".claude/skills/paper-claims/SKILL.md").is_file())
        self.assertTrue((root / ".agents/skills/paper-claims/SKILL.md").is_file())
        self.assertIn(kit.POINTER_MARKER, (root / "AGENTS.md").read_text())
        self.assertIn("@.paperkit/AGENTS.md", (root / "CLAUDE.md").read_text())
        cfg = json.loads((root / kit.CONFIG).read_text())
        self.assertEqual(cfg["venue"], "isca")
        self.assertEqual(cfg["agents"], ["claude", "codex"])
        manifest = json.loads((root / kit.MANIFEST).read_text())["files"]
        self.assertIn(".paperkit/memory/guidelines.md", manifest)
        self.assertTrue((root / "paper").is_dir())

    def test_init_keeps_existing_agents_md_loaded_by_claude(self):
        root = self.tmp / "paper-repo"
        root.mkdir()
        (root / "AGENTS.md").write_text("Project rules.\n")
        self.assertEqual(run("init", str(root), "--no-git")[0], 0)
        claude = (root / "CLAUDE.md").read_text()
        self.assertTrue(claude.startswith("@AGENTS.md\n"), claude)
        self.assertTrue((root / "AGENTS.md").read_text().startswith("Project rules.\n"))

    def test_init_twice_refuses(self):
        root = self.init()
        code, out = run("init", str(root), "--no-git")
        self.assertEqual(code, 1)
        self.assertIn("already a paperkit project", out)

    def test_unknown_venue_rejected(self):
        code, out = run("init", str(self.tmp / "x"), "--no-git", "--venue", "nope")
        self.assertEqual(code, 1)
        self.assertIn("unknown venue", out)


class UpgradeTests(Base):
    def test_upgrade_noop(self):
        self.init()
        code, out = run("upgrade")
        self.assertEqual(code, 0)
        self.assertIn("already up to date", out)

    def test_unmodified_file_is_updated_edited_file_is_kept(self):
        root = self.init()
        venue = root / ".paperkit/venues/isca.md"
        guide = root / ".paperkit/memory/guidelines.md"
        # Simulate an older kit version: both files recorded with old content.
        manifest_path = root / kit.MANIFEST
        data = json.loads(manifest_path.read_text())
        venue.write_text("old kit text\n")
        data["files"][".paperkit/venues/isca.md"] = kit.sha256_file(venue)
        manifest_path.write_text(json.dumps(data))
        # User edits the guidelines after install.
        guide.write_text(guide.read_text() + "\nMY RULE\n")

        code, out = run("upgrade", "--dry-run")
        self.assertIn("would update", out)
        self.assertEqual(venue.read_text(), "old kit text\n")

        code, out = run("upgrade")
        self.assertEqual(code, 0, out)
        self.assertNotEqual(venue.read_text(), "old kit text\n")
        self.assertIn("MY RULE", guide.read_text())
        self.assertIn("keep edited", out)
        self.assertTrue((root / ".paperkit/memory/guidelines.md.paperkit-new").is_file())

    def test_legacy_bootstrap_install_migrates_constitution(self):
        root = self.tmp / "legacy"
        (root / ".paperkit/memory").mkdir(parents=True)
        (root / ".paperkit/memory/constitution.md").write_text("# Paper Constitution\nMINE\n")
        os.chdir(root)
        code, out = run("upgrade")
        self.assertEqual(code, 0, out)
        g = root / ".paperkit/memory/guidelines.md"
        self.assertTrue(g.is_file())
        self.assertFalse((root / ".paperkit/memory/constitution.md").exists())
        self.assertTrue(g.read_text().startswith("# Paper Guidelines\nMINE"))
        self.assertTrue((root / ".paperkit/memory/guidelines.md.paperkit-new").is_file())


class AgentTests(Base):
    def test_add_and_remove_codex(self):
        root = self.init()
        self.assertFalse((root / ".agents/skills").exists())
        self.assertEqual(run("agent", "add", "codex")[0], 0)
        self.assertTrue((root / ".agents/skills/paper-review/SKILL.md").is_file())
        self.assertEqual(run("agent", "remove", "codex")[0], 0)
        self.assertFalse((root / ".agents").exists())
        self.assertTrue((root / ".claude/skills/paper-review/SKILL.md").is_file())

    def test_remove_claude_drops_pointer(self):
        root = self.init("--ai", "claude,codex")
        run("agent", "remove", "claude")
        self.assertFalse((root / ".claude/skills").exists())
        claude = root / "CLAUDE.md"
        self.assertTrue(not claude.exists() or kit.POINTER_MARKER not in claude.read_text())


class UninstallTests(Base):
    def test_uninstall_keeps_edits_and_paper(self):
        root = self.init()
        (root / "paper/claims.md").write_text("mine\n")
        guide = root / ".paperkit/memory/guidelines.md"
        guide.write_text("edited\n")
        self.assertEqual(run("uninstall")[0], 1)  # needs --yes
        code, out = run("uninstall", "--yes")
        self.assertEqual(code, 0, out)
        self.assertTrue(guide.is_file())
        self.assertTrue((root / "paper/claims.md").is_file())
        self.assertFalse((root / ".paperkit/venues").exists())
        self.assertFalse((root / ".claude").exists())
        self.assertFalse((root / "CLAUDE.md").exists())
        self.assertFalse((root / "AGENTS.md").exists())


CLAIMS = """# Claims
| ID | Claim | Status | Evidence | Shortcuts named | Where it appears |
| --- | --- | --- | --- | --- | --- |
| H1 | [one falsifiable sentence] | [M/D/E/U/C] | x | x | x |
| H2 | Batched serving doubles at 42 robots | M | fig 18 | none | abstract |
| H3 | Edge placement wins | U | TBD | none | intro |
| S1 | Link RTT 1.8 ms | M | link data | none | H2 |
| S2 | Energy per call | E | TBD | none | H3 |
"""
VENUE = """# Target venue: ISCA 2027
| Constraint | Value | Source |
| --- | --- | --- |
| Deadline | 2026-11-20 AoE | CFP |
| Page limit | UNVERIFIED: CFP not posted | CFP |
"""
FIGURES = """| ID | Type | Takeaway | Claims | Data file | Built by | Status |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | plot | x | H2 | d | s | final |
| F2 | plot | x | H3 | d | s | planned |
"""
REVIEW = """| # | Severity | Finding | Location | Claim threatened | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | reject | weak baseline | 6 | H2 | run vLLM |
| 2 | minor | caption | F1 | H2 | reword |
"""


class StatusTests(Base):
    def test_parsers(self):
        c = st.parse_claims(CLAIMS)
        self.assertEqual(c["headline"]["M"], 1)
        self.assertEqual(c["headline"]["U"], 1)
        self.assertEqual(c["supporting"]["E"], 1)
        self.assertEqual(c["unset"], 1)
        self.assertEqual(c["blockers"], ["H3 is a headline claim with status U"])
        v = st.parse_venue(VENUE, dt.date(2026, 10, 28))
        self.assertEqual(v["name"], "ISCA 2027")
        self.assertEqual(v["days_left"], 23)
        self.assertEqual(v["unverified"], 1)
        f = st.parse_figures(FIGURES)
        self.assertEqual((f["final"], f["planned"]), (1, 1))
        r = st.parse_review(REVIEW)
        self.assertEqual((r["reject"], r["minor"]), (1, 1))
        self.assertEqual(st.parse_check("## Result\n\nFAIL: 2 items\n"), "FAIL")

    def test_status_next_phase_progression(self):
        root = self.init("--venue", "isca")
        rep = st.collect(root)
        self.assertEqual(rep["next"], "/paper-venue")
        (root / "paper/venue.md").write_text(VENUE)
        (root / "paper/claims.md").write_text(CLAIMS)
        self.assertEqual(st.collect(root)["next"], "/paper-outline")
        (root / "paper/outline.md").write_text("x")
        (root / "paper/figures.md").write_text(FIGURES)
        rep = st.collect(root, today=dt.date(2026, 10, 28))
        self.assertEqual(rep["next"], "/paper-claims")  # headline blocker
        self.assertEqual(rep["tbd"], 2)
        code, out = run("status")
        self.assertEqual(code, 0)
        self.assertIn("headline M1 U1", out)
        self.assertIn("next: /paper-claims", out)
        code, out = run("status", "--json")
        self.assertEqual(json.loads(out)["phases"]["figures"]["final"], 1)


class MiscTests(Base):
    def test_scan_flags_banned_terms(self):
        root = self.init()
        (root / "main.tex").write_text("Each treatment ran. % campaign ignored\n")
        code, out = run("scan")
        # scan runs in a subprocess; its output goes to the real stdout
        self.assertEqual(code, 1)

    def test_venue_and_agent_lists(self):
        code, out = run("venue", "list")
        self.assertEqual(code, 0)
        self.assertIn("isca", out)
        self.assertNotIn("_template", out)
        self.assertIn("claude", run("agent", "list")[1])

    def test_venue_use(self):
        root = self.init()
        self.assertEqual(run("venue", "use", "mlsys")[0], 0)
        self.assertEqual(json.loads((root / kit.CONFIG).read_text())["venue"], "mlsys")

    def test_check_and_version(self):
        self.assertIn(run("check")[0], (0, 1))
        code, out = run("version", "--json")
        self.assertEqual(code, 0)
        self.assertIn("pk", json.loads(out))

    def test_outside_project(self):
        os.chdir(self.tmp)
        code, out = run("status")
        self.assertEqual(code, 1)
        self.assertIn("pk init", out)

    def test_phase_gate_script_still_works(self):
        root = self.init()
        out = subprocess.run(["bash", ".paperkit/scripts/bash/check-prerequisites.sh", "--phase", "venue"],
                             cwd=root, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(json.loads(out.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
