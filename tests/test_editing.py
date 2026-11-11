"""Editorial regressions: protect results while allowing useful prose edits."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from paperkit import edit_check
from paperkit import install as kit
from paperkit import status as st
from test_cli import Base, run


BEFORE = r"""It is worth noting that our modelled median decision latency is
8 ms on the Orin-class SoC with TensorRT FP16, compared with 10 ms for FIFO
under the same configuration (Figure~\ref{fig:latency}). This excludes dispatch
and the control tick. See \cite{queue2025,policy2026}.
\label{sec:results}
\[ L = t_{queue} + t_{service} \]
"""
AFTER = r"""With TensorRT FP16 on the Orin-class SoC, our modelled median decision
latency is 8 ms, compared with 10 ms for FIFO under the same configuration
(Figure~\ref{fig:latency}). This excludes dispatch and the control tick.
See \cite{queue2025,policy2026}.
\label{sec:results}
\[ L = t_{queue} + t_{service} \]
"""


class PreservationTests(Base):
    def test_architecture_revision_keeps_its_scientific_tokens(self):
        rep = edit_check.compare(BEFORE, AFTER, terms=("decision latency", "FIFO"))
        self.assertEqual(rep["result"], "PASS", rep)

    def test_scientific_changes_require_review(self):
        mutations = [
            ("8 ms", "6 ms", "numbers"),
            ("8 ms", "8 cycles", "quantities"),
            ("modelled", "measured", "qualifiers"),
            ("median", "mean", "qualifiers"),
            (r"\cite{queue2025,policy2026}", r"\cite{queue2025}", "citations"),
            ("fig:latency", "fig:throughput", "references"),
            ("sec:results", "sec:overview", "labels"),
            ("t_{queue} + t_{service}", "t_{queue} - t_{service}", "math"),
            ("decision\nlatency", "inference time", "terms"),
        ]
        for old, new, category in mutations:
            with self.subTest(category=category):
                self.assertIn(old, AFTER)
                rep = edit_check.compare(BEFORE, AFTER.replace(old, new), terms=("decision latency",))
                self.assertEqual(rep["result"], "REVIEW", rep)
                self.assertIn(category, rep["changes"])

    def test_duplicate_or_added_results_are_not_set_equality(self):
        for extra in (" Another run took 8 ms.", r" Another source is \cite{queue2025}."):
            self.assertEqual(edit_check.compare(BEFORE, AFTER + extra)["result"], "REVIEW")

    def test_tex_comments_and_escaped_percentages(self):
        self.assertEqual(edit_check.compare("A result. % 99 ms\n", "A result. % 20 ms\n")["result"], "PASS")
        self.assertEqual(edit_check.compare(r"Gain 5\%.", r"Gain 6\%.")["result"], "REVIEW")
        # A LaTeX line break does not escape a subsequent comment marker.
        self.assertEqual(edit_check.compare("A \\\\% 99\n", "A \\\\% 20\n")["result"], "PASS")

    def test_quantities_scientific_notation_and_spelled_terms(self):
        for before, after in (("2e-3 s", "2e-4 s"), ("4 GiB", "4 MiB"),
                              ("16 cores", "32 cores"), (".5 W", ".6 W"), ("4 GHz", "4 MHz"),
                              ("-2 cycles", "+2 cycles"), ("1,024 bytes", "1,025 bytes")):
            with self.subTest(before=before):
                self.assertEqual(edit_check.compare(before, after)["result"], "REVIEW")
        self.assertEqual(edit_check.compare("2.", "3.")["result"], "REVIEW")
        self.assertEqual(edit_check.compare("two cores", "three cores", terms=("two cores",))["result"], "REVIEW")

    def test_citation_reordering_is_allowed_but_counts_and_keys_are_preserved(self):
        self.assertEqual(edit_check.compare(r"\citep{a2,b3}", r"\citep{b3,a2}")["result"], "PASS")
        rep = edit_check.compare(r"\textcite{a2}", r"\textcite{b3}")
        self.assertEqual(rep["result"], "REVIEW")
        self.assertNotIn("numbers", rep["changes"])
        self.assertEqual(edit_check.compare(r"\citep[p. 2]{a2}", r"\citep[p. 3]{a2}")["result"], "REVIEW")

    def test_math_forms_and_input_paths(self):
        for before, after in (("$a+b$", "$a-b$"), (r"\(a+b\)", r"\(a-b\)"),
                              ("$$a+b$$", "$$a-b$$"),
                              (r"\begin{align*}a&=b\end{align*}", r"\begin{align*}a&=c\end{align*}"),
                              (r"\input{eval}", r"\input{design}")):
            with self.subTest(before=before):
                self.assertEqual(edit_check.compare(before, after)["result"], "REVIEW")

    def test_markdown_percent_is_not_a_tex_comment(self):
        self.assertEqual(edit_check.compare("After 5%, 12 runs.", "After 5%, 14 runs.", latex=False)["result"], "REVIEW")

    def test_same_tokens_cannot_establish_scientific_equivalence(self):
        # Deliberately document the boundary: a human must inspect associations
        # and negation even when every protected token matches.
        rep = edit_check.compare("FIFO takes 8 ms; ours takes 10 ms.",
                                 "FIFO takes 10 ms; ours takes 8 ms.")
        self.assertEqual(rep["result"], "PASS")
        self.assertIn("number-to-result associations", rep["limitation"])
        self.assertEqual(edit_check.compare("The cache does not stall.", "The cache does stall.")["result"], "PASS")

    def test_cli_outputs_real_hashes_and_handles_missing_inputs(self):
        before, after = self.tmp / "before.tex", self.tmp / "after.tex"
        before.write_text(BEFORE, encoding="utf-8")
        after.write_text(AFTER, encoding="utf-8")
        code, out = run("edit-check", str(before), str(after), "--term", "decision latency", "--json")
        self.assertEqual(code, 0, out)
        rep = json.loads(out)
        self.assertEqual(rep["before"]["sha256"], kit.sha256_file(before))
        self.assertEqual(rep["after"]["sha256"], kit.sha256_file(after))
        self.assertNotEqual(rep["before"]["sha256"], rep["after"]["sha256"])
        after.write_text(AFTER.replace("8 ms", "6 ms"), encoding="utf-8")
        self.assertEqual(run("edit-check", str(before), str(after))[0], 1)
        self.assertEqual(run("edit-check", str(before), str(before))[0], 2)
        self.assertEqual(run("edit-check", str(before), str(self.tmp / "missing.tex"))[0], 2)
        self.assertEqual(run("edit-check", str(before), str(self.tmp / "wrong.md"))[0], 2)


class EditingIntegrationTests(Base):
    def test_both_agents_receive_edit_skill_and_shared_resources(self):
        root = self.init("--ai", "claude,codex")
        for agent_dir in kit.AGENT_SKILL_DIRS.values():
            self.assertTrue((root / agent_dir / "paper-edit/SKILL.md").is_file())
        for rel in ("memory/architecture-writing.md", "memory/prose-patterns.tsv",
                    "templates/voice-template.md", "templates/edit-report-template.md",
                    "THIRD_PARTY_NOTICES.md"):
            self.assertTrue((root / ".paperkit" / rel).is_file())

    def test_upgrade_adds_editing_without_overwriting_author_voice(self):
        root = self.init("--ai", "claude,codex")
        # Model a pre-editing install, then upgrade it with the new kit.
        missing = ".agents/skills/paper-edit/SKILL.md"
        (root / missing).unlink()
        manifest_path = root / kit.MANIFEST
        manifest = json.loads(manifest_path.read_text())
        manifest["files"].pop(missing)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        voice = root / "paper/voice.md"
        voice.write_text("Prefer direct section openings.\n", encoding="utf-8")
        self.assertEqual(run("upgrade")[0], 0)
        self.assertTrue((root / missing).is_file())
        self.assertEqual(voice.read_text(), "Prefer direct section openings.\n")
        self.assertEqual(run("uninstall", "--yes")[0], 0)
        self.assertTrue(voice.is_file())

    def test_editing_is_optional_and_does_not_change_phase_progression(self):
        root = self.init()
        self.assertEqual(st.collect(root)["next"], "/paper-venue")
        (root / "paper/voice.md").write_text("Author preferences.\n")
        (root / "paper/edit-20261110-120000.md").write_text("An audit, not a gate.\n")
        rep = st.collect(root)
        self.assertEqual(rep["next"], "/paper-venue")
        self.assertTrue(rep["editing"]["voice_profile"])
        self.assertIn("not a gate", st.render(rep))

    def test_generic_prose_warns_but_architecture_terms_remain_valid(self):
        root = self.init()
        source = root / "main.tex"
        source.write_text("In recent years, cache design changed. Furthermore, we evaluate it.\n"
                          "The out-of-order pipeline uses speculative execution.\n", encoding="utf-8")
        script = root / ".paperkit/scripts/bash/scan_text.py"
        rep = subprocess.run([sys.executable, str(script), str(root)], capture_output=True, text=True)
        self.assertEqual(rep.returncode, 0, rep.stdout + rep.stderr)
        self.assertIn("main.tex:1: warn:", rep.stdout)
        self.assertNotIn("main.tex:2:", rep.stdout)
        source.write_text("Each treatment ran.\n", encoding="utf-8")
        self.assertEqual(subprocess.run([sys.executable, str(script), str(root)],
                                       capture_output=True).returncode, 1)

    def test_edit_gate_requires_evidence_artifacts_but_not_voice_samples(self):
        root = self.init()
        cmd = ["bash", ".paperkit/scripts/bash/check-prerequisites.sh", "--phase", "edit"]
        rep = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        self.assertEqual(rep.returncode, 1, rep.stderr)
        self.assertEqual(json.loads(rep.stdout)["missing"], ["venue", "claims"])
        (root / "paper/venue.md").write_text("Venue verified.\n")
        (root / "paper/claims.md").write_text("Claims.\n")
        rep = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        self.assertEqual(rep.returncode, 0, rep.stderr)
        self.assertTrue(json.loads(rep.stdout)["ok"])
