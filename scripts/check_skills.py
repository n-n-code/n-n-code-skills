#!/usr/bin/env python3
"""Validate the repository skill inventory and documentation contracts."""

import re
import subprocess
import sys
from dataclasses import dataclass
from difflib import get_close_matches
from pathlib import Path
from typing import List, Optional, Sequence, Set, Tuple, Union

REQUIRED_REPO_FILES = (
    "scripts/check_skills.py",
    "scripts/check-skills.sh",
    "scripts/test_check_skills.py",
)
ROOT_INVENTORY_TOKENS = {
    ".agents": ".agents/skills/",
    "scripts": "scripts/",
    "README.md": "README.md",
    "AGENTS.md": "AGENTS.md",
    "LICENSE": "LICENSE",
}
IGNORED_TOP_LEVEL_ENTRIES = {".git", ".pytest_cache", "__pycache__"}
# Command names intentionally used in routing prose, not published skill names.
NON_SKILL_ROUTING_TERMS = {"playwright-cli", "state-save"}
SKILL_REF_PATTERN = re.compile(r"^[a-z][a-z0-9]+(?:-[a-z0-9]+)+$")
MARKDOWN_CANDIDATE_PATTERN = re.compile(
    r"\x60([^\x60\n]+)\x60|\*\*([^*\n]+)\*\*"
)
ROUTING_PREFIX_PATTERN = re.compile(
    r"(?:"
    r"\b(?:use|load|select|choose|expected|add)\s+"
    r"(?:the\s+)?(?:skill\s+)?(?:named\s+)?"
    r"|\b(?:compose|pair)\s+with\s+"
    r"|\bstart\s+with\s+"
    r")$",
    re.IGNORECASE,
)
ROUTING_SUFFIX_PATTERN = re.compile(
    r"^\s*(?::|,)?\s*(?:skill\b|as\s+(?:the\s+)?(?:primary|companion)\b)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ValidationResult:
    errors: Tuple[str, ...]
    skill_count: int


def check_frontmatter_lines(
    skill_file: Union[Path, str],
    frontmatter_lines: Sequence[str],
    start_line: int = 2,
) -> Tuple[List[str], List[str]]:
    """Validate the repository's deliberately small frontmatter contract."""
    errors: List[str] = []
    keys: List[str] = []

    for line_no, line in enumerate(frontmatter_lines, start_line):
        if not line.strip():
            continue

        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not match:
            errors.append(
                f"{skill_file}:{line_no}: frontmatter lines must use "
                "simple key: value syntax"
            )
            continue

        key, value = match.groups()
        keys.append(key)

        if key not in {"name", "description"}:
            continue

        value = value.strip()
        quoted = (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        )
        if not value:
            errors.append(
                f"{skill_file}:{line_no}: frontmatter {key} value must not be empty"
            )
        if ": " in value and not quoted:
            errors.append(
                f"{skill_file}:{line_no}: frontmatter {key} value containing "
                "': ' must be quoted"
            )
        if value[:1] in {"'", '"'} and not quoted:
            errors.append(
                f"{skill_file}:{line_no}: frontmatter {key} value has an "
                "unterminated quote"
            )

    if keys != ["name", "description"]:
        errors.append(
            f"{skill_file}: frontmatter keys must be exactly name, description; "
            f"got {keys}"
        )

    return keys, errors


def check_required_repo_files(root: Path) -> List[str]:
    errors: List[str] = []
    for relative_path in REQUIRED_REPO_FILES:
        path = root / relative_path
        if not path.is_file():
            errors.append(f"missing required repository file {path}")
    return errors


def check_skill_packages(
    root: Path,
) -> Tuple[List[Path], Set[str], List[str]]:
    skills_dir = root / ".agents" / "skills"
    errors: List[str] = []
    skill_dirs: List[Path] = []
    skill_names: Set[str] = set()

    if not skills_dir.is_dir():
        return skill_dirs, skill_names, ["missing .agents/skills directory"]

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    skill_names = {path.name for path in skill_dirs}
    if not skill_dirs:
        errors.append("no skill folders found under .agents/skills")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue

        try:
            lines = skill_file.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{skill_file}: could not read UTF-8 text: {exc}")
            continue

        if len(lines) < 4 or lines[0] != "---":
            errors.append(f"{skill_file}: missing opening YAML frontmatter")
            continue

        try:
            end = lines[1:].index("---") + 1
        except ValueError:
            errors.append(f"{skill_file}: missing closing YAML frontmatter")
            continue

        _, frontmatter_errors = check_frontmatter_lines(skill_file, lines[1:end])
        errors.extend(frontmatter_errors)

        name_line = next(
            (line for line in lines[1:end] if line.startswith("name:")),
            "",
        )
        declared_name = name_line.split(":", 1)[1].strip() if ":" in name_line else ""
        if declared_name != skill_dir.name:
            errors.append(
                f"{skill_file}: frontmatter name {declared_name!r} does not "
                f"match folder {skill_dir.name!r}"
            )

    return skill_dirs, skill_names, errors


def git_tracked_files(root: Path) -> Optional[List[str]]:
    """Return tracked files, or None when Git cannot provide the inventory."""
    try:
        completed = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None

    if completed.returncode != 0:
        return None
    return completed.stdout.splitlines()


def current_top_level_entries(root: Path) -> Set[str]:
    return {
        path.name
        for path in root.iterdir()
        if path.name not in IGNORED_TOP_LEVEL_ENTRIES
    }


def check_readme_inventory(
    root: Path,
    readme_text: str,
    skill_dirs: Sequence[Path],
) -> List[str]:
    """Check current files first, with Git adding tracked-but-absent context."""
    errors: List[str] = []

    for skill_dir in skill_dirs:
        if f"\x60{skill_dir.name}\x60" not in readme_text:
            errors.append(
                f"README.md: missing published skill \x60{skill_dir.name}\x60"
            )

    top_level_entries = current_top_level_entries(root)
    tracked_files = git_tracked_files(root)
    if tracked_files is not None:
        top_level_entries.update(
            path.split("/", 1)[0] for path in tracked_files if path
        )

    for entry in sorted(top_level_entries):
        token = ROOT_INVENTORY_TOKENS.get(entry, entry)
        if token not in readme_text:
            errors.append(
                f"README.md: missing current top-level inventory entry for {entry!r}"
            )

    scripts_dir = root / "scripts"
    if scripts_dir.is_dir():
        script_files = sorted(
            path for path in scripts_dir.iterdir() if path.is_file()
        )
        for script_file in script_files:
            relative_path = script_file.relative_to(root).as_posix()
            if relative_path not in readme_text:
                errors.append(
                    "README.md: missing current script inventory entry for "
                    f"{relative_path!r}"
                )

    return errors


def collect_markdown_sources(root: Path) -> List[Path]:
    sources = list(root.glob(".agents/skills/**/*.md"))
    sources.extend(
        path for path in (root / "README.md", root / "AGENTS.md") if path.is_file()
    )
    return sorted(sources)


def check_relative_links(sources: Sequence[Path]) -> List[str]:
    errors: List[str] = []

    for path in sources:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: could not read UTF-8 text: {exc}")
            continue

        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).strip()
            target_path = target.split("#", 1)[0]
            if (
                not target_path
                or re.match(r"^[a-z][a-z0-9+.-]*:", target_path)
                or target_path.startswith("/")
            ):
                continue
            target_path = target_path.strip("<>")
            if not (path.parent / target_path).exists():
                errors.append(f"{path}: broken relative link to {target}")

    return errors


def looks_like_routing_reference(
    line: str,
    candidate_start: int,
    candidate_end: int,
) -> bool:
    prefix = line[:candidate_start]
    suffix = line[candidate_end:]
    return bool(
        ROUTING_PREFIX_PATTERN.search(prefix)
        or ROUTING_SUFFIX_PATTERN.match(suffix)
    )


def check_skill_references(
    sources: Sequence[Path],
    skill_names: Set[str],
) -> List[str]:
    """Report explicit routing references and likely typos, not every kebab term."""
    errors: List[str] = []

    for path in sources:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: could not read UTF-8 text: {exc}")
            continue

        for line_no, line in enumerate(lines, 1):
            for match in MARKDOWN_CANDIDATE_PATTERN.finditer(line):
                group = 1 if match.group(1) is not None else 2
                candidate = match.group(group).strip()
                if not SKILL_REF_PATTERN.match(candidate):
                    continue
                if candidate in NON_SKILL_ROUTING_TERMS:
                    continue
                if candidate in skill_names:
                    continue

                start, end = match.span()
                close_match = get_close_matches(
                    candidate,
                    sorted(skill_names),
                    n=1,
                    cutoff=0.84,
                )
                if not close_match and not looks_like_routing_reference(
                    line,
                    start,
                    end,
                ):
                    continue

                hint = (
                    f"; nearest published skill is {close_match[0]!r}"
                    if close_match
                    else ""
                )
                errors.append(
                    f"{path}:{line_no}: possible unknown skill reference "
                    f"\x60{candidate}\x60{hint}"
                )

    return errors


def read_required(path: Path, errors: List[str]) -> str:
    if not path.is_file():
        errors.append(f"missing {path}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: could not read UTF-8 text: {exc}")
        return ""


def require_contains(
    path: Path,
    text: str,
    needle: str,
    label: str,
    errors: List[str],
) -> None:
    if needle not in text:
        errors.append(f"{path}: missing story-family invariant: {label}")


def require_compact_contains(
    path: Path,
    text: str,
    needle: str,
    label: str,
    errors: List[str],
) -> None:
    compact_text = re.sub(r"\s+", " ", text)
    compact_needle = re.sub(r"\s+", " ", needle)
    if compact_needle not in compact_text:
        errors.append(f"{path}: missing story-family invariant: {label}")


def require_absent(
    path: Path,
    text: str,
    needle: str,
    label: str,
    errors: List[str],
) -> None:
    if needle in text:
        errors.append(f"{path}: forbidden story-family regression: {label}")


def check_repo_specific_invariants(
    root: Path,
    sources: Sequence[Path],
) -> List[str]:
    errors: List[str] = []
    skills_dir = root / ".agents" / "skills"
    trigger_eval = (
        skills_dir
        / "agent-skill-generator"
        / "references"
        / "inventory-trigger-evals.md"
    )
    if not trigger_eval.is_file():
        errors.append(f"missing {trigger_eval}")

    story_skill_paths = {
        "clarifier": skills_dir / "user-story-clarifier" / "SKILL.md",
        "scout": skills_dir / "story-repo-scout" / "SKILL.md",
        "planner": skills_dir / "story-implementation-planner" / "SKILL.md",
        "orchestrator": skills_dir / "story-implementation-orchestrator" / "SKILL.md",
    }
    story_texts = {
        name: read_required(path, errors)
        for name, path in story_skill_paths.items()
    }

    for path in sources:
        text = read_required(path, errors)
        require_absent(
            path,
            text,
            "superpowers:",
            "legacy superpowers references",
            errors,
        )

    clarifier_text = story_texts["clarifier"]
    require_contains(
        story_skill_paths["clarifier"],
        clarifier_text,
        "Status: Split Candidate",
        "split packets keep top-level Split Candidate status",
        errors,
    )
    require_contains(
        story_skill_paths["clarifier"],
        clarifier_text,
        "- Status: Ready | Needs Clarification | Blocked",
        "split slices carry their own readiness status",
        errors,
    )

    orchestrator_text = story_texts["orchestrator"]
    require_contains(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "Materialize the selected slice as the active story card before scouting",
        "selected split slices are materialized before scouting",
        errors,
    )
    require_contains(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "Pass one materialized story card for the active slice",
        "scouting input is the active materialized slice, not the whole split set",
        errors,
    )
    require_contains(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "\x60First Action\x60 block present when",
        "orchestrator validates First Action conditionally",
        errors,
    )
    require_compact_contains(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "optional for agent profiles, and absent for\n  \x60human\x60",
        "human plans omit First Action in orchestrator readiness",
        errors,
    )
    require_contains(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "Default for repo-owned code changes: \x60project-core-dev\x60",
        "project-core-dev routing is conditional on code changes",
        errors,
    )
    require_contains(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "Workflow overlay: \x60tester-mindset\x60 when",
        "tester-mindset routing is conditional",
        errors,
    )
    require_absent(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "- Always: \x60project-core-dev\x60",
        "unconditional project-core-dev routing",
        errors,
    )
    require_absent(
        story_skill_paths["orchestrator"],
        orchestrator_text,
        "- Always: \x60tester-mindset\x60",
        "unconditional tester-mindset routing",
        errors,
    )

    scout_text = story_texts["scout"]
    require_contains(
        story_skill_paths["scout"],
        scout_text,
        "\x60None identified\x60 when this output will feed",
        "Do Not Touch can explicitly report no boundary found",
        errors,
    )
    require_compact_contains(
        story_skill_paths["scout"],
        scout_text,
        "Likely Unrelated / Do\nNot Touch\x60 as \x60None identified\x60",
        "orchestrated packets preserve the None identified convention",
        errors,
    )

    planner_text = story_texts["planner"]
    require_contains(
        story_skill_paths["planner"],
        planner_text,
        "Required for \x60local-small\x60, optional for agent profiles",
        "planner treats First Action as executor-specific",
        errors,
    )
    require_contains(
        story_skill_paths["planner"],
        planner_text,
        "omitted for \x60human\x60",
        "human plans omit First Action",
        errors,
    )
    require_contains(
        story_skill_paths["planner"],
        planner_text,
        "repo-owned code changes",
        "planner routes project-core-dev only for repo-owned code changes",
        errors,
    )
    require_contains(
        story_skill_paths["planner"],
        planner_text,
        "Add \x60tester-mindset\x60 when",
        "planner routes tester-mindset conditionally",
        errors,
    )
    require_absent(
        story_skill_paths["planner"],
        planner_text,
        "must hand off to \x60project-core-dev\x60",
        "unconditional project-core-dev planner handoff",
        errors,
    )

    return errors


def validate_repository(root: Path) -> ValidationResult:
    root = root.resolve()
    errors: List[str] = []

    errors.extend(check_required_repo_files(root))
    skill_dirs, skill_names, skill_errors = check_skill_packages(root)
    errors.extend(skill_errors)

    readme = root / "README.md"
    if readme.is_file():
        try:
            readme_text = readme.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{readme}: could not read UTF-8 text: {exc}")
        else:
            errors.extend(check_readme_inventory(root, readme_text, skill_dirs))
    else:
        errors.append("missing README.md")

    sources = collect_markdown_sources(root)
    errors.extend(check_relative_links(sources))
    errors.extend(check_skill_references(sources, skill_names))
    errors.extend(check_repo_specific_invariants(root, sources))

    return ValidationResult(tuple(errors), len(skill_dirs))


def main(root: Optional[Path] = None) -> int:
    repository_root = root or Path(__file__).resolve().parents[1]
    result = validate_repository(repository_root)

    if result.errors:
        for error in result.errors:
            print(f"check-skills: {error}", file=sys.stderr)
        return 1

    print(f"check-skills: ok ({result.skill_count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
