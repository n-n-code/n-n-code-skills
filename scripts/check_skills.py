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
GUIDANCE_DESCRIPTION_NEIGHBORS = {
    "backend-guidance": "backend-systems-guidance",
    "backend-systems-guidance": "backend-guidance",
    "coding-guidance-bash": "project-release-maintainer",
    "coding-guidance-cpp": "coding-guidance-qt",
    "coding-guidance-go": "coding-guidance-go-tui",
    "coding-guidance-go-tui": "coding-guidance-go",
    "coding-guidance-qt": "coding-guidance-cpp",
    "ui-design-guidance": "ui-guidance",
    "ui-guidance": "ui-design-guidance",
}
GUIDANCE_REVIEW_BOUNDARY_PATTERN = re.compile(
    r"(?:read-only|do\s+not\s+edit|without\s+editing)",
    re.IGNORECASE,
)
GO_TUI_ONE_SHOT_HUH_PATTERN = re.compile(
    r"(?:standalone|one-shot)[^.\n]*Huh|Huh[^.\n]*(?:standalone|one-shot)",
    re.IGNORECASE,
)
README_GUIDANCE_REVIEW_CONTRACT = (
    "For review-only work, guidance skills report prioritized evidence-backed "
    "findings without editing files or requiring findings to be fixed."
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


def frontmatter_description(text: str) -> str:
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("'\"")


def check_guidance_family_invariants(
    root: Path,
    readme_text: str,
) -> List[str]:
    """Protect stable routing and read-only contracts for guidance skills."""
    errors: List[str] = []
    skills_dir = root / ".agents" / "skills"

    for skill_dir in sorted(skills_dir.glob("*guidance*")):
        skill_file = skill_dir / "SKILL.md"
        text = read_required(skill_file, errors)
        if not text:
            continue

        description = frontmatter_description(text)
        if "review" not in description.lower():
            errors.append(
                f"{skill_file}: missing guidance-family invariant: "
                "frontmatter description must expose review capability"
            )
        if not GUIDANCE_REVIEW_BOUNDARY_PATTERN.search(text):
            errors.append(
                f"{skill_file}: missing guidance-family invariant: "
                "review requests need an explicit read-only boundary"
            )

        neighbor = GUIDANCE_DESCRIPTION_NEIGHBORS.get(skill_dir.name)
        if neighbor and neighbor not in description:
            errors.append(
                f"{skill_file}: missing guidance-family invariant: "
                f"description must route against {neighbor!r}"
            )

        if (
            skill_dir.name == "coding-guidance-go-tui"
            and not GO_TUI_ONE_SHOT_HUH_PATTERN.search(description)
        ):
            errors.append(
                f"{skill_file}: missing guidance-family invariant: "
                "description must exclude standalone or one-shot Huh prompts"
            )

    compact_readme = re.sub(r"\s+", " ", readme_text)
    if README_GUIDANCE_REVIEW_CONTRACT not in compact_readme:
        errors.append(
            f"{root / 'README.md'}: missing guidance-family invariant: "
            "shared review-only contract"
        )

    return errors


def require_contains(
    path: Path,
    text: str,
    needle: str,
    label: str,
    errors: List[str],
) -> None:
    if needle not in text:
        errors.append(f"{path}: missing story-family invariant: {label}")


def require_section_contains(
    path: Path,
    text: str,
    start_marker: str,
    end_marker: Optional[str],
    needle: str,
    label: str,
    errors: List[str],
) -> None:
    start = text.find(start_marker)
    if start < 0:
        errors.append(f"{path}: missing story-family invariant: {label}")
        return

    end = text.find(end_marker, start + len(start_marker)) if end_marker else -1
    section = text[start:] if end < 0 else text[start:end]
    if needle not in section:
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


def check_packet_example_semantics(path: Path, text: str) -> List[str]:
    """Check the example's dependency graph and validation mapping."""
    errors: List[str] = []
    steps_start = text.find("### Steps")
    steps_end = text.find("### Dependencies and Parallel Work", steps_start)
    if steps_start < 0 or steps_end < 0:
        return errors

    steps: dict[str, Optional[List[str]]] = {}
    current_step: Optional[str] = None
    for line in text[steps_start:steps_end].splitlines():
        step_match = re.match(r"^\d+\. `([A-Za-z][A-Za-z0-9-]*) - ", line)
        if step_match:
            current_step = step_match.group(1)
            if current_step in steps:
                errors.append(
                    f"{path}: invalid packet example: duplicate step ID "
                    f"{current_step}"
                )
            steps[current_step] = None
            continue

        blocker_match = re.match(r"^\s+- Blocked by:\s*(.*?)\s*$", line)
        if blocker_match and current_step:
            raw_blockers = blocker_match.group(1).rstrip(".").strip()
            steps[current_step] = (
                []
                if raw_blockers == "None"
                else [
                    item.strip().strip("`")
                    for item in raw_blockers.split(",")
                    if item.strip()
                ]
            )

    if not steps:
        errors.append(f"{path}: invalid packet example: no plan steps found")
        return errors

    for step_id, blockers in steps.items():
        if blockers is None:
            errors.append(
                f"{path}: invalid packet example: {step_id} has no Blocked by edge"
            )

    graph = {
        step_id: blockers or []
        for step_id, blockers in steps.items()
    }
    known_ids = set(graph)
    for step_id, blockers in graph.items():
        for blocker in blockers:
            if blocker not in known_ids:
                errors.append(
                    f"{path}: invalid packet example: {step_id} has unknown "
                    f"blocker {blocker}"
                )
            elif blocker == step_id:
                errors.append(
                    f"{path}: invalid packet example: {step_id} blocks itself"
                )

    state: dict[str, int] = {}

    def visit(step_id: str) -> bool:
        if state.get(step_id) == 1:
            return True
        if state.get(step_id) == 2:
            return False
        state[step_id] = 1
        for blocker in graph[step_id]:
            if blocker in graph and visit(blocker):
                return True
        state[step_id] = 2
        return False

    if any(visit(step_id) for step_id in graph if state.get(step_id) != 2):
        errors.append(f"{path}: invalid packet example: blocker graph has a cycle")

    def reaches(source: str, target: str) -> bool:
        pending = list(graph.get(source, []))
        seen: Set[str] = set()
        while pending:
            candidate = pending.pop()
            if candidate == target:
                return True
            if candidate in seen or candidate not in graph:
                continue
            seen.add(candidate)
            pending.extend(graph[candidate])
        return False

    for step_id, blockers in graph.items():
        for blocker in blockers:
            if any(
                other != blocker and reaches(other, blocker)
                for other in blockers
            ):
                errors.append(
                    f"{path}: invalid packet example: {step_id} has redundant "
                    f"transitive blocker {blocker}"
                )

    dependency_text = text[steps_end:]
    frontier_match = re.search(
        r"(?m)^- Starting frontier:\s*(.*?)\s*$",
        dependency_text,
    )
    if frontier_match:
        raw_frontier = frontier_match.group(1).rstrip(".").strip()
        actual_frontier = {
            item.strip().strip("`")
            for item in raw_frontier.split(",")
            if item.strip() and raw_frontier != "None"
        }
        expected_frontier = {
            step_id for step_id, blockers in graph.items() if not blockers
        }
        if actual_frontier != expected_frontier:
            errors.append(
                f"{path}: invalid packet example: starting frontier "
                f"{sorted(actual_frontier)} does not match unblocked steps "
                f"{sorted(expected_frontier)}"
            )

    validation_start = text.find("### Acceptance Criteria and Validation")
    validation_end = text.find("### Delivery and Recovery", validation_start)
    if validation_start >= 0:
        validation_text = (
            text[validation_start:]
            if validation_end < 0
            else text[validation_start:validation_end]
        )
        mapped_criteria: Set[str] = set()
        for line in validation_text.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if not cells or not re.fullmatch(r"(?:S\d+-)?AC-\d+", cells[0]):
                continue
            mapped_criteria.add(cells[0])
            if len(cells) < 4 or not cells[2] or cells[2] in {"-", "None"}:
                errors.append(
                    f"{path}: invalid packet example: {cells[0]} has a blank "
                    "validation seam"
                )

        story_end = text.find("## Repo Context")
        story_text = text[:story_end] if story_end >= 0 else text
        story_criteria = set(
            re.findall(r"(?m)^- ((?:S\d+-)?AC-\d+):", story_text)
        )
        missing_criteria = story_criteria - mapped_criteria
        if missing_criteria:
            errors.append(
                f"{path}: invalid packet example: acceptance criteria missing "
                f"validation rows: {sorted(missing_criteria)}"
            )

    return errors


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
    trigger_eval_text = read_required(trigger_eval, errors)

    story_skill_paths = {
        "clarifier": skills_dir / "story-clarifier" / "SKILL.md",
        "scout": skills_dir / "story-repo-scout" / "SKILL.md",
        "planner": skills_dir / "story-implementation-planner" / "SKILL.md",
        "orchestrator": skills_dir / "story-to-plan-orchestrator" / "SKILL.md",
    }
    story_texts = {
        name: read_required(path, errors)
        for name, path in story_skill_paths.items()
    }
    packet_example_path = (
        skills_dir
        / "story-to-plan-orchestrator"
        / "references"
        / "story-to-plan-packet-example.md"
    )
    packet_example_text = read_required(packet_example_path, errors)

    for retired_name in (
        "user-story-clarifier",
        "story-implementation-orchestrator",
    ):
        retired_path = skills_dir / retired_name
        if retired_path.exists():
            errors.append(
                f"{retired_path}: retired story skill must not coexist with its "
                "replacement"
            )

    for needle, label in (
        ("## Story Clarification", "story clarification trigger cases"),
        ("Expected `story-clarifier`:", "story clarifier trigger owner"),
        ("## Story Repo Scouting", "story repo-scout trigger cases"),
        ("Expected `story-repo-scout`:", "story repo-scout trigger owner"),
        ("## Story Implementation Planning", "story planning trigger cases"),
        (
            "Expected `story-implementation-planner`:",
            "story planner trigger owner",
        ),
        ("## Story-To-Plan Orchestration", "story orchestration trigger cases"),
        (
            "Expected `story-to-plan-orchestrator`:",
            "story orchestrator trigger owner",
        ),
        ("### Story-Family Routing Matrix", "story-family state routing cases"),
    ):
        require_contains(trigger_eval, trigger_eval_text, needle, label, errors)

    for needle, label in (
        (
            "Expected not `story-clarifier` as primary:",
            "story clarifier adjacent-negative cases",
        ),
        (
            "Expected not `story-repo-scout` as primary:",
            "story repo-scout adjacent-negative cases",
        ),
        (
            "Expected not `story-implementation-planner` as primary:",
            "story planner adjacent-negative cases",
        ),
        (
            "Expected not `story-to-plan-orchestrator` as primary:",
            "story orchestrator adjacent-negative cases",
        ),
        ("Collision cases:", "story-family collision cases"),
        (
            "Instruction behavior after explicit selection:",
            "story-family post-selection behavior cases",
        ),
    ):
        require_section_contains(
            trigger_eval,
            trigger_eval_text,
            "## Story Clarification",
            "## Project Overlays",
            needle,
            label,
            errors,
        )

    for path in sources:
        text = read_required(path, errors)
        require_absent(
            path,
            text,
            "superpowers:",
            "legacy superpowers references",
            errors,
        )

    component_protocol = (
        "Status: Ready | Needs Input | Blocked",
        "Reason: None | <concise readiness reason>",
    )
    for name in ("clarifier", "scout", "planner"):
        for needle in component_protocol:
            require_contains(
                story_skill_paths[name],
                story_texts[name],
                needle,
                f"{name} preserves the common story-family artifact protocol",
                errors,
            )

    clarifier_text = story_texts["clarifier"]
    for needle, label in (
        ("**Synthesize:**", "clarifier supports source-only synthesis"),
        ("Artifact Type: Story Card", "clarifier owns the Story Card artifact"),
        (
            "Artifact Type: Split Story Set",
            "clarifier keeps split-set shape separate from readiness",
        ),
        ("## Slice Dependencies", "clarifier records slice blocker edges"),
        ("- External prerequisites: None", "clarifier separates external slice prerequisites"),
        (
            "[Not yet specifiable]",
            "clarifier separates in-scope fog from sharp questions",
        ),
        ("Artifact Type: Story Audit", "clarifier labels audit-only output"),
        ("## Audit Output", "clarifier defines non-rewriting audit behavior"),
    ):
        require_contains(
            story_skill_paths["clarifier"],
            clarifier_text,
            needle,
            label,
            errors,
        )
    story_card_source_token = (
        "Source: <inline | conversation | path | issue URL | external identifier "
        "and revision | inherited from parent Split Story Set | None>"
    )
    direct_source_token = (
        "Source: <inline | conversation | path | issue URL | external identifier "
        "and revision | None>"
    )
    for start_marker, end_marker, needle, label in (
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
    ):
        require_section_contains(
            story_skill_paths["clarifier"],
            clarifier_text,
            start_marker,
            end_marker,
            needle,
            label,
            errors,
        )
    scout_text = story_texts["scout"]
    for needle, label in (
        ("Artifact Type: Repo Context", "scout owns the Repo Context artifact"),
        ("## Existing Evidence", "scout separates inspected existing evidence"),
        (
            "## External Evidence",
            "scout separates planning-critical external primary evidence",
        ),
        (
            "| Evidence ID | Claim | Owning Primary Source and Section | Applicable Version/Date | Planning Consequence |",
            "scout records stable claim-level external provenance",
        ),
        ("## Proposed Paths", "scout grounds files that do not yet exist"),
        (
            "| Evidence Type | Source | Observable Seam or Behavior | Prior-Art Basis and Limits |",
            "scout records validation seams as prior art",
        ),
        (
            "## Authoritative Constraints / Do Not Edit",
            "scout distinguishes authoritative boundaries from nearby non-targets",
        ),
        (
            "`Direct`:",
            "scout defines evidence strength independently from story readiness",
        ),
    ):
        require_contains(
            story_skill_paths["scout"],
            scout_text,
            needle,
            label,
            errors,
        )
    planner_text = story_texts["planner"]
    for needle, label in (
        (
            "Artifact Type: Implementation Plan",
            "planner owns the Implementation Plan artifact",
        ),
        ("## Executor Constraints", "planner adapts to evidenced executor constraints"),
        (
            "- External primary evidence:",
            "planner traces decision-bearing external claims",
        ),
        ("Proposed Create", "planner supports convention-backed new files"),
        ("- Blocked by:", "planner records direct blocker edges"),
        ("- Starting frontier:", "planner derives an executable frontier"),
        (
            "| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |",
            "planner selects validation seams explicitly",
        ),
        ("### Blocking Inputs", "planner separates blockers from manageable risks"),
    ):
        require_contains(
            story_skill_paths["planner"],
            planner_text,
            needle,
            label,
            errors,
        )
    orchestrator_text = story_texts["orchestrator"]
    for needle, label in (
        ("## Ownership", "orchestrator assigns one owner per stage artifact"),
        (
            "## Invalidation And Resumption",
            "orchestrator owns dependency invalidation and packet resumption",
        ),
        (
            "Artifact Type: Preparation Packet",
            "orchestrator labels its assembled packet",
        ),
        ("## Pending Stage", "orchestrator preserves non-ready stage state"),
        (
            "| `story-clarifier` | Story Card or Split Story Set |",
            "orchestrator maps the story artifact to its owner",
        ),
        (
            "| `story-repo-scout` | Repo Context |",
            "orchestrator maps repo context to its owner",
        ),
        (
            "| `story-implementation-planner` | Implementation Plan |",
            "orchestrator maps the plan artifact to its owner",
        ),
    ):
        require_contains(
            story_skill_paths["orchestrator"],
            orchestrator_text,
            needle,
            label,
            errors,
        )
    for needle, label in (
        ("Artifact Type: Preparation Packet", "packet example labels the packet"),
        ("Artifact Type: Story Card", "packet example includes a story artifact"),
        ("Artifact Type: Repo Context", "packet example includes repo context"),
        (
            "Artifact Type: Implementation Plan",
            "packet example includes an implementation plan",
        ),
        ("Source: conversation", "packet example preserves story provenance"),
        ("- Starting frontier:", "packet example demonstrates blocker frontier"),
        (
            "| Acceptance Criterion | Planned Outcome | Validation Seam | Validation Evidence |",
            "packet example demonstrates validation-seam mapping",
        ),
        (
            "- External prerequisites:",
            "packet example records external-prerequisite satisfaction",
        ),
    ):
        require_contains(
            packet_example_path,
            packet_example_text,
            needle,
            label,
            errors,
        )
    errors.extend(
        check_packet_example_semantics(packet_example_path, packet_example_text)
    )
    return errors


def validate_repository(root: Path) -> ValidationResult:
    root = root.resolve()
    errors: List[str] = []

    errors.extend(check_required_repo_files(root))
    skill_dirs, skill_names, skill_errors = check_skill_packages(root)
    errors.extend(skill_errors)

    readme = root / "README.md"
    readme_text = ""
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
    errors.extend(check_guidance_family_invariants(root, readme_text))
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
