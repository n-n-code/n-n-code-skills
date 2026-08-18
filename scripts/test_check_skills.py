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


if __name__ == "__main__":
    unittest.main()
