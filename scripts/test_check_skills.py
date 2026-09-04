#!/usr/bin/env python3
"""Focused regression tests for the repository skill validator."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_skills  # noqa: E402


class CheckSkillsTests(unittest.TestCase):
    def test_frontmatter_rejects_raw_nonprintable_metadata(self) -> None:
        for char in ("\x00", "\x01", "\x0b", "\x0c", "\x1f", "\x7f", "\x80", "\x9f", "\ud800", "\ufffe", "\uffff"):
            for value in (f"alpha{char}beta", f"'alpha{char}beta'", f'"alpha{char}beta"'):
                with self.subTest(value=ascii(value)):
                    _, errors = check_skills.check_frontmatter_lines(
                        "example/SKILL.md", ["name: example", f"description: {value}"]
                    )
                    self.assertTrue(errors, ascii(value))

    def test_frontmatter_rejects_colon_tab_separator(self) -> None:
        _, errors = check_skills.check_frontmatter_lines(
            "example/SKILL.md", ["name: example", "description: alpha:\tbeta"]
        )
        self.assertTrue(errors)

    def test_package_preserves_invalid_controls_for_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = root / ".agents" / "skills" / "example"
            skill.mkdir(parents=True)
            for char in ("\x0b", "\x0c", "\x1c", "\x1d", "\x1e"):
                with self.subTest(character=ascii(char)):
                    (skill / "SKILL.md").write_text(
                        f"---\nname: example\ndescription: Useful guidance.{char}\n---\nInspect input.\n",
                        encoding="utf-8",
                    )
                    _, _, errors = check_skills.check_skill_packages(root)
                    self.assertTrue(errors)

    def test_frontmatter_preserves_legal_unicode_and_quoted_tabs(self) -> None:
        for value in ("Review café, 日本語, and 🧪 examples.", "'alpha:\tbeta'", r'"alpha:\tbeta"'):
            with self.subTest(value=value):
                _, errors = check_skills.check_frontmatter_lines(
                    "example/SKILL.md", ["name: example", f"description: {value}"]
                )
                self.assertEqual(errors, [])

    def test_frontmatter_enforces_name_and_description_limits(self) -> None:
        for name, description, valid in (
            ("a" * 64, "x" * 1024, True),
            ("a" * 65, "Useful guidance.", False),
            ("valid-skill", "x" * 1025, False),
            ("Bad-Skill", "Useful guidance.", False),
            ("bad--skill", "Useful guidance.", False),
            ("-bad", "Useful guidance.", False),
            ("bad-", "Useful guidance.", False),
            ("bad_name", "Useful guidance.", False),
        ):
            with self.subTest(name=name, description_length=len(description)):
                _, errors = check_skills.check_frontmatter_lines(
                    "example/SKILL.md",
                    [f"name: {name}", f"description: {description}"],
                )
                self.assertEqual(not errors, valid, errors)

    def test_frontmatter_requires_string_scalars(self) -> None:
        for value in (
            "[one, two]", "{key: value}", "true", "null", "~", "42",
            "2026-09-04", "1:20", ".inf", "0x10", "# comment", "- list",
            "Text # hidden comment", "|", ">", "*alias", "&anchor text",
            "'unterminated", '"bad\\q"', "''", '"   "',
        ):
            with self.subTest(value=value):
                _, errors = check_skills.check_frontmatter_lines(
                    "example/SKILL.md", ["name: example", f"description: {value}"]
                )
                self.assertTrue(errors, value)

    def test_frontmatter_accepts_quoted_strings_and_literal_punctuation(self) -> None:
        for value in (
            '"Use this: preserve the contract."',
            "'Review the user''s code.'",
            '"true"',
            "Review C# and C++ code with `tool-name`.",
            "2026-09-04 compatibility guidance.",
            "1:20 is an example duration.",
        ):
            with self.subTest(value=value):
                _, errors = check_skills.check_frontmatter_lines(
                    "example/SKILL.md", ["name: example", f"description: {value}"]
                )
                self.assertEqual(errors, [])

    def test_package_matches_decoded_quoted_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / ".agents" / "skills" / "example"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                '---\nname: "example"\ndescription: Useful guidance.\n---\n'
                '\nInspect the input and report the result.\n', encoding="utf-8"
            )
            _, _, errors = check_skills.check_skill_packages(root)
        self.assertEqual(errors, [])

    def test_package_rejects_empty_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / ".agents" / "skills" / "example"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                '---\nname: example\ndescription: Useful guidance.\n---\n\n',
                encoding="utf-8",
            )
            _, _, errors = check_skills.check_skill_packages(root)
        self.assertTrue(any("instructions" in error for error in errors), errors)

    def test_frontmatter_rejects_unquoted_colon_and_empty_description(self) -> None:
        _, errors = check_skills.check_frontmatter_lines(
            "example/SKILL.md",
            ["name: example", "description: bad: value"],
        )
        self.assertTrue(
            any("value containing ': ' must be quoted" in error for error in errors)
        )

        _, empty_errors = check_skills.check_frontmatter_lines(
            "example/SKILL.md",
            ["name: example", "description:"],
        )
        self.assertTrue(
            any(
                "description value must not be empty" in error
                for error in empty_errors
            )
        )

    def test_untracked_script_must_be_documented(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            scripts_dir = root / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "new_tool.py").write_text("", encoding="utf-8")

            with patch.object(check_skills, "git_tracked_files", return_value=[]):
                errors = check_skills.check_readme_inventory(
                    root,
                    "scripts/\n",
                    [],
                )

        self.assertTrue(
            any("scripts/new_tool.py" in error for error in errors),
            errors,
        )

    def test_git_absence_falls_back_to_current_filesystem(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "NOTES.md").write_text("notes", encoding="utf-8")

            with patch.object(
                check_skills.subprocess,
                "run",
                side_effect=FileNotFoundError,
            ):
                self.assertIsNone(check_skills.git_tracked_files(root))

            with patch.object(check_skills, "git_tracked_files", return_value=None):
                errors = check_skills.check_readme_inventory(root, "", [])

        self.assertTrue(
            any("NOTES.md" in error for error in errors),
            errors,
        )

    def test_broken_relative_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "README.md"
            source.write_text("[missing](missing.md)\n", encoding="utf-8")
            errors = check_skills.check_relative_links([source])

        self.assertTrue(any("broken relative link" in error for error in errors))

    def test_likely_skill_typo_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "README.md"
            source.write_text("Expected `known-skll`:\n", encoding="utf-8")
            errors = check_skills.check_skill_references(
                [source],
                {"known-skill"},
            )

        self.assertTrue(any("known-skll" in error for error in errors), errors)
        self.assertTrue(any("known-skill" in error for error in errors), errors)

    def test_explicit_unknown_skill_reference_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "README.md"
            source.write_text("Use `not-published-skill`.\n", encoding="utf-8")
            errors = check_skills.check_skill_references(
                [source],
                {"known-skill"},
            )

        self.assertTrue(any("not-published-skill" in error for error in errors))

    def test_non_skill_kebab_term_is_not_treated_as_routing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "README.md"
            source.write_text(
                "Use the skill to record `host-observed` results.\n",
                encoding="utf-8",
            )
            errors = check_skills.check_skill_references(
                [source],
                {"known-skill"},
            )

        self.assertEqual(errors, [])

    def test_known_non_skill_command_is_not_treated_as_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "README.md"
            source.write_text("Use `playwright-cli`.\n", encoding="utf-8")
            errors = check_skills.check_skill_references(
                [source],
                {"known-skill"},
            )

        self.assertEqual(errors, [])

    def test_guidance_family_requires_neighbor_and_review_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / ".agents" / "skills" / "ui-guidance"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: ui-guidance\n"
                "description: Routine UI implementation and review guidance.\n"
                "---\n"
                "\n# UI Guidance\n",
                encoding="utf-8",
            )

            errors = check_skills.check_guidance_family_invariants(root, "")

        self.assertTrue(
            any("ui-design-guidance" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("read-only boundary" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("shared review-only contract" in error for error in errors),
            errors,
        )

    def test_go_tui_description_requires_one_shot_huh_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / ".agents" / "skills" / "coding-guidance-go-tui"
            skill_dir.mkdir(parents=True)
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(
                "---\n"
                "name: coding-guidance-go-tui\n"
                "description: Go TUI implementation and review; use "
                "coding-guidance-go for other work.\n"
                "---\n"
                "\nReview requests are read-only.\n",
                encoding="utf-8",
            )
            readme = check_skills.README_GUIDANCE_REVIEW_CONTRACT

            errors = check_skills.check_guidance_family_invariants(root, readme)

        self.assertTrue(
            any("one-shot Huh" in error for error in errors),
            errors,
        )

    def _write_story_family_fixture(self, root: Path) -> dict[str, Path]:
        skills_dir = root / ".agents" / "skills"
        trigger_eval = (
            skills_dir
            / "agent-skill-generator"
            / "references"
            / "inventory-trigger-evals.md"
        )
        trigger_eval.parent.mkdir(parents=True)
        trigger_eval.write_text(
            "## Story Clarification\n"
            "Expected `story-clarifier`:\n"
            "Expected not `story-clarifier` as primary:\n"
            "## Story Repo Scouting\n"
            "Expected `story-repo-scout`:\n"
            "Expected not `story-repo-scout` as primary:\n"
            "## Story Implementation Planning\n"
            "Expected `story-implementation-planner`:\n"
            "Expected not `story-implementation-planner` as primary:\n"
            "## Story-To-Plan Orchestration\n"
            "Expected `story-to-plan-orchestrator`:\n"
            "Expected not `story-to-plan-orchestrator` as primary:\n"
            "### Story-Family Routing Matrix\n"
            "Collision cases:\n"
            "Instruction behavior after explicit selection:\n"
            "## Project Overlays\n",
            encoding="utf-8",
        )

        shared_protocol = (
            "Status: Ready | Needs Input | Blocked\n"
            "Reason: None | <concise readiness reason>\n"
        )
        story_card_source_token = (
            "Source: <inline | conversation | path | issue URL | external "
            "identifier and revision | inherited from parent Split Story Set | None>\n"
        )
        direct_source_token = (
            "Source: <inline | conversation | path | issue URL | external "
            "identifier and revision | None>\n"
        )
        fixtures = {
            "story-clarifier": (
                shared_protocol
                + "**Synthesize:**\n"
                + "## Story Card Contract\n"
                + "Artifact Type: Story Card\n"
                + story_card_source_token
                + "## Split Story Set Contract\n"
                + "Artifact Type: Split Story Set\n"
                + direct_source_token
                + "## Slice Dependencies\n"
                + "- External prerequisites: None\n"
                + "## Ready and Ambiguity Rules\n"
                + "[Not yet specifiable]\n"
                + "## Audit Output\n"
                + "Artifact Type: Story Audit\n"
                + direct_source_token
                + "## Composition Boundaries\n"
            ),
            "story-repo-scout": (
                shared_protocol
                + "Artifact Type: Repo Context\n"
                + "## Existing Evidence\n"
                + "## External Evidence\n"
                + "| Evidence ID | Claim | Owning Primary Source and Section | Applicable Version/Date | Planning Consequence |\n"
                + "## Proposed Paths\n"
                + "| Evidence Type | Source | Observable Seam or Behavior | Prior-Art Basis and Limits |\n"
                + "## Authoritative Constraints / Do Not Edit\n"
                + "`Direct`:\n"
            ),
            "story-implementation-planner": (
                shared_protocol
                + "Artifact Type: Implementation Plan\n"
                + "## Executor Constraints\n"
                + "- External primary evidence:\n"
                + "Proposed Create\n"
                + "- Blocked by:\n"
                + "- Starting frontier:\n"
                + "| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |\n"
                + "### Blocking Inputs\n"
            ),
            "story-to-plan-orchestrator": (
                "## Ownership\n"
                "## Invalidation And Resumption\n"
                "Artifact Type: Preparation Packet\n"
                "## Pending Stage\n"
                "| `story-clarifier` | Story Card or Split Story Set |\n"
                "| `story-repo-scout` | Repo Context |\n"
                "| `story-implementation-planner` | Implementation Plan |\n"
            ),
        }
        paths = {"trigger-evals": trigger_eval}
        for name, text in fixtures.items():
            skill_dir = skills_dir / name
            skill_dir.mkdir(parents=True)
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(text, encoding="utf-8")
            paths[name] = skill_file
        packet_example = (
            skills_dir
            / "story-to-plan-orchestrator"
            / "references"
            / "story-to-plan-packet-example.md"
        )
        packet_example.parent.mkdir(parents=True, exist_ok=True)
        packet_example.write_text(
            "Artifact Type: Preparation Packet\n"
            "Status: Ready\n"
            "Reason: None\n"
            "## Story Card\n"
            "Artifact Type: Story Card\n"
            "Source: conversation\n"
            "### Acceptance Criteria\n"
            "- AC-1: Fixture behavior is observable.\n"
            "## Repo Context\n"
            "Artifact Type: Repo Context\n"
            "## Implementation Plan\n"
            "Artifact Type: Implementation Plan\n"
            "### Steps\n"
            "1. `P1 - First outcome` - establish the first behavior.\n"
            "   - Blocked by: None.\n"
            "2. `P2 - Second outcome` - extend the behavior.\n"
            "   - Blocked by: P1.\n"
            "3. `P3 - Third outcome` - complete the behavior.\n"
            "   - Blocked by: P2.\n"
            "### Dependencies and Parallel Work\n"
            "- Starting frontier: P1.\n"
            "- External prerequisites: None.\n"
            "### Acceptance Criteria and Validation\n"
            "| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |\n"
            "|---|---|---|---|\n"
            "| AC-1 | P3 | existing integration seam | fixture assertion |\n"
            "### Delivery and Recovery\n",
            encoding="utf-8",
        )
        paths["packet-example"] = packet_example
        return paths

    def test_story_family_invariants_follow_artifact_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_story_family_fixture(root)

            errors = check_skills.check_repo_specific_invariants(root, [])

        self.assertEqual(errors, [])

    def test_story_family_invariants_reject_contract_token_removal(self) -> None:
        cases = (
            (
                "trigger-evals",
                "## Story Clarification",
                "story clarification trigger cases",
            ),
            (
                "trigger-evals",
                "Expected `story-clarifier`:",
                "story clarifier trigger owner",
            ),
            (
                "trigger-evals",
                "Expected not `story-clarifier` as primary:",
                "story clarifier adjacent-negative cases",
            ),
            (
                "trigger-evals",
                "## Story Repo Scouting",
                "story repo-scout trigger cases",
            ),
            (
                "trigger-evals",
                "Expected `story-repo-scout`:",
                "story repo-scout trigger owner",
            ),
            (
                "trigger-evals",
                "Expected not `story-repo-scout` as primary:",
                "story repo-scout adjacent-negative cases",
            ),
            (
                "trigger-evals",
                "## Story Implementation Planning",
                "story planning trigger cases",
            ),
            (
                "trigger-evals",
                "Expected `story-implementation-planner`:",
                "story planner trigger owner",
            ),
            (
                "trigger-evals",
                "Expected not `story-implementation-planner` as primary:",
                "story planner adjacent-negative cases",
            ),
            (
                "trigger-evals",
                "## Story-To-Plan Orchestration",
                "story orchestration trigger cases",
            ),
            (
                "trigger-evals",
                "Expected `story-to-plan-orchestrator`:",
                "story orchestrator trigger owner",
            ),
            (
                "trigger-evals",
                "Expected not `story-to-plan-orchestrator` as primary:",
                "story orchestrator adjacent-negative cases",
            ),
            (
                "trigger-evals",
                "### Story-Family Routing Matrix",
                "story-family state routing cases",
            ),
            (
                "trigger-evals",
                "Collision cases:",
                "story-family collision cases",
            ),
            (
                "trigger-evals",
                "Instruction behavior after explicit selection:",
                "story-family post-selection behavior cases",
            ),
            (
                "story-clarifier",
                "**Synthesize:**",
                "clarifier supports source-only synthesis",
            ),
            (
                "story-clarifier",
                "Artifact Type: Story Card",
                "clarifier owns the Story Card artifact",
            ),
            (
                "story-clarifier",
                "Artifact Type: Split Story Set",
                "clarifier keeps split-set shape separate",
            ),
            (
                "story-clarifier",
                "## Slice Dependencies",
                "clarifier records slice blocker edges",
            ),
            (
                "story-clarifier",
                "- External prerequisites: None",
                "clarifier separates external slice prerequisites",
            ),
            (
                "story-clarifier",
                "[Not yet specifiable]",
                "clarifier separates in-scope fog from sharp questions",
            ),
            (
                "story-clarifier",
                "Artifact Type: Story Audit",
                "clarifier labels audit-only output",
            ),
            (
                "story-clarifier",
                "## Audit Output",
                "clarifier defines non-rewriting audit behavior",
            ),
            (
                "story-repo-scout",
                "Artifact Type: Repo Context",
                "scout owns the Repo Context artifact",
            ),
            (
                "story-repo-scout",
                "## Existing Evidence",
                "scout separates inspected existing evidence",
            ),
            (
                "story-repo-scout",
                "## External Evidence",
                "scout separates planning-critical external primary evidence",
            ),
            (
                "story-repo-scout",
                "| Evidence ID | Claim | Owning Primary Source and Section | Applicable Version/Date | Planning Consequence |",
                "scout records stable claim-level external provenance",
            ),
            (
                "story-repo-scout",
                "## Proposed Paths",
                "scout grounds files that do not yet exist",
            ),
            (
                "story-repo-scout",
                "| Evidence Type | Source | Observable Seam or Behavior | Prior-Art Basis and Limits |",
                "scout records validation seams as prior art",
            ),
            (
                "story-repo-scout",
                "## Authoritative Constraints / Do Not Edit",
                "scout distinguishes authoritative boundaries",
            ),
            (
                "story-repo-scout",
                "`Direct`:",
                "scout defines evidence strength",
            ),
            (
                "story-implementation-planner",
                "Artifact Type: Implementation Plan",
                "planner owns the Implementation Plan artifact",
            ),
            (
                "story-implementation-planner",
                "## Executor Constraints",
                "planner adapts to evidenced executor constraints",
            ),
            (
                "story-implementation-planner",
                "- External primary evidence:",
                "planner traces decision-bearing external claims",
            ),
            (
                "story-implementation-planner",
                "Proposed Create",
                "planner supports convention-backed new files",
            ),
            (
                "story-implementation-planner",
                "- Blocked by:",
                "planner records direct blocker edges",
            ),
            (
                "story-implementation-planner",
                "- Starting frontier:",
                "planner derives an executable frontier",
            ),
            (
                "story-implementation-planner",
                "| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |",
                "planner selects validation seams explicitly",
            ),
            (
                "story-implementation-planner",
                "### Blocking Inputs",
                "planner separates blockers",
            ),
            (
                "story-to-plan-orchestrator",
                "## Ownership",
                "orchestrator assigns one owner",
            ),
            (
                "story-to-plan-orchestrator",
                "## Invalidation And Resumption",
                "orchestrator owns dependency invalidation",
            ),
            (
                "story-to-plan-orchestrator",
                "Artifact Type: Preparation Packet",
                "orchestrator labels its assembled packet",
            ),
            (
                "story-to-plan-orchestrator",
                "## Pending Stage",
                "orchestrator preserves non-ready stage state",
            ),
            (
                "story-to-plan-orchestrator",
                "| `story-clarifier` | Story Card or Split Story Set |",
                "orchestrator maps the story artifact",
            ),
            (
                "story-to-plan-orchestrator",
                "| `story-repo-scout` | Repo Context |",
                "orchestrator maps repo context",
            ),
            (
                "story-to-plan-orchestrator",
                "| `story-implementation-planner` | Implementation Plan |",
                "orchestrator maps the plan artifact",
            ),
            (
                "packet-example",
                "Artifact Type: Preparation Packet",
                "packet example labels the packet",
            ),
            (
                "packet-example",
                "Artifact Type: Story Card",
                "packet example includes a story artifact",
            ),
            (
                "packet-example",
                "Artifact Type: Repo Context",
                "packet example includes repo context",
            ),
            (
                "packet-example",
                "Artifact Type: Implementation Plan",
                "packet example includes an implementation plan",
            ),
            (
                "packet-example",
                "Source: conversation",
                "packet example preserves story provenance",
            ),
            (
                "packet-example",
                "- Starting frontier:",
                "packet example demonstrates blocker frontier",
            ),
            (
                "packet-example",
                "| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |",
                "packet example demonstrates validation-seam mapping",
            ),
            (
                "packet-example",
                "- External prerequisites:",
                "packet example records external-prerequisite satisfaction",
            ),
        )
        protocol_cases = tuple(
            (
                name,
                token,
                f"{role} preserves the common story-family artifact protocol",
            )
            for name, role in (
                ("story-clarifier", "clarifier"),
                ("story-repo-scout", "scout"),
                ("story-implementation-planner", "planner"),
            )
            for token in (
                "Status: Ready | Needs Input | Blocked",
                "Reason: None | <concise readiness reason>",
            )
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = self._write_story_family_fixture(root)
            for fixture_name, token, expected_error in cases + protocol_cases:
                with self.subTest(fixture=fixture_name, token=token):
                    path = paths[fixture_name]
                    original = path.read_text(encoding="utf-8")
                    path.write_text(original.replace(token, "", 1), encoding="utf-8")
                    try:
                        errors = check_skills.check_repo_specific_invariants(
                            root,
                            [],
                        )

                        self.assertTrue(
                            any(expected_error in error for error in errors),
                            errors,
                        )
                    finally:
                        path.write_text(original, encoding="utf-8")

    def test_story_family_invariants_require_source_in_each_clarifier_artifact(
        self,
    ) -> None:
        story_card_source_token = (
            "Source: <inline | conversation | path | issue URL | external "
            "identifier and revision | inherited from parent Split Story Set | None>"
        )
        direct_source_token = (
            "Source: <inline | conversation | path | issue URL | external "
            "identifier and revision | None>"
        )
        cases = (
            (
                "## Story Card Contract",
                "## Split Story Set Contract",
                story_card_source_token,
                "clarifier requires Story Card source provenance",
            ),
            (
                "## Split Story Set Contract",
                "## Ready and Ambiguity Rules",
                direct_source_token,
                "clarifier requires Split Story Set source provenance",
            ),
            (
                "## Audit Output",
                "## Composition Boundaries",
                direct_source_token,
                "clarifier requires Story Audit source provenance",
            ),
        )

        for start_marker, end_marker, source_token, expected_error in cases:
            with self.subTest(section=start_marker):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    paths = self._write_story_family_fixture(root)
                    path = paths["story-clarifier"]
                    original = path.read_text(encoding="utf-8")
                    start = original.index(start_marker)
                    end = original.index(end_marker, start + len(start_marker))
                    section = original[start:end]
                    self.assertIn(source_token, section)
                    mutated_section = section.replace(source_token, "", 1)
                    path.write_text(
                        original[:start] + mutated_section + original[end:],
                        encoding="utf-8",
                    )
                    try:
                        errors = check_skills.check_repo_specific_invariants(
                            root,
                            [],
                        )
                        self.assertTrue(
                            any(expected_error in error for error in errors),
                            errors,
                        )
                    finally:
                        path.write_text(original, encoding="utf-8")

    def _assert_packet_mutation_error(
        self,
        old: str,
        new: str,
        expected_error: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = self._write_story_family_fixture(root)
            path = paths["packet-example"]
            original = path.read_text(encoding="utf-8")
            self.assertIn(old, original)
            path.write_text(original.replace(old, new, 1), encoding="utf-8")
            try:
                errors = check_skills.check_repo_specific_invariants(root, [])
                self.assertTrue(
                    any(expected_error in error for error in errors),
                    errors,
                )
            finally:
                path.write_text(original, encoding="utf-8")

    def test_packet_example_rejects_unknown_blocker(self) -> None:
        self._assert_packet_mutation_error(
            "   - Blocked by: P1.\n",
            "   - Blocked by: P9.\n",
            "unknown blocker P9",
        )

    def test_packet_example_rejects_blocker_cycle(self) -> None:
        self._assert_packet_mutation_error(
            "   - Blocked by: None.\n",
            "   - Blocked by: P3.\n",
            "blocker graph has a cycle",
        )

    def test_packet_example_rejects_redundant_transitive_blocker(self) -> None:
        self._assert_packet_mutation_error(
            "   - Blocked by: P2.\n",
            "   - Blocked by: P1, P2.\n",
            "redundant transitive blocker P1",
        )

    def test_packet_example_rejects_false_starting_frontier(self) -> None:
        self._assert_packet_mutation_error(
            "- Starting frontier: P1.\n",
            "- Starting frontier: P2.\n",
            "starting frontier",
        )

    def test_packet_example_rejects_blank_validation_seam(self) -> None:
        self._assert_packet_mutation_error(
            "| AC-1 | P3 | existing integration seam | fixture assertion |\n",
            "| AC-1 | P3 |  | fixture assertion |\n",
            "AC-1 has a blank validation seam",
        )

    def test_story_family_invariants_require_trigger_evals(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = self._write_story_family_fixture(root)
            paths["trigger-evals"].unlink()

            errors = check_skills.check_repo_specific_invariants(root, [])

        self.assertTrue(
            any(
                "missing" in error and "inventory-trigger-evals.md" in error
                for error in errors
            ),
            errors,
        )

    def test_story_family_invariants_reject_retired_alias_packages(self) -> None:
        for retired_name in (
            "user-story-clarifier",
            "story-implementation-orchestrator",
        ):
            with self.subTest(retired_name=retired_name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    self._write_story_family_fixture(root)
                    retired_dir = root / ".agents" / "skills" / retired_name
                    retired_dir.mkdir(parents=True)

                    errors = check_skills.check_repo_specific_invariants(root, [])

                self.assertTrue(
                    any(
                        retired_name in error and "must not coexist" in error
                        for error in errors
                    ),
                    errors,
                )


if __name__ == "__main__":
    unittest.main()
