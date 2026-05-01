#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

if ! command -v python3 >/dev/null 2>&1; then
  printf 'check-skills: python3 is required for markdown/link checks\n' >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
import re
import subprocess
import sys

root = Path(".")
skills_dir = root / ".agents" / "skills"
errors = []
skill_names = set()

def check_frontmatter_lines(skill_file, frontmatter_lines, start_line=2):
    frontmatter_errors = []
    keys = []

    for line_no, line in enumerate(frontmatter_lines, start_line):
        if not line.strip():
            continue

        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not match:
            frontmatter_errors.append(
                f"{skill_file}:{line_no}: frontmatter lines must use simple key: value syntax"
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
        if ": " in value and not quoted:
            frontmatter_errors.append(
                f"{skill_file}:{line_no}: frontmatter {key} value containing ': ' must be quoted"
            )
        if value[:1] in {"'", '"'} and not quoted:
            frontmatter_errors.append(
                f"{skill_file}:{line_no}: frontmatter {key} value has an unterminated quote"
            )

    if keys != ["name", "description"]:
        frontmatter_errors.append(
            f"{skill_file}: frontmatter keys must be exactly name, description; got {keys}"
        )

    return keys, frontmatter_errors

self_test_keys, self_test_errors = check_frontmatter_lines(
    "frontmatter-self-test/SKILL.md",
    ["name: frontmatter-self-test", "description: bad: value"],
)
if self_test_keys != ["name", "description"] or not any(
    "value containing ': ' must be quoted" in error for error in self_test_errors
):
    errors.append("frontmatter self-test failed to catch unquoted ': ' in description")

if not skills_dir.is_dir():
    errors.append("missing .agents/skills directory")
else:
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    skill_names = {path.name for path in skill_dirs}
    if not skill_dirs:
        errors.append("no skill folders found under .agents/skills")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue

        lines = skill_file.read_text(encoding="utf-8").splitlines()
        if len(lines) < 4 or lines[0] != "---":
            errors.append(f"{skill_file}: missing opening YAML frontmatter")
            continue

        try:
            end = lines[1:].index("---") + 1
        except ValueError:
            errors.append(f"{skill_file}: missing closing YAML frontmatter")
            continue

        keys, frontmatter_errors = check_frontmatter_lines(skill_file, lines[1:end])
        errors.extend(frontmatter_errors)

        name_line = next(
            (line for line in lines[1:end] if line.startswith("name:")),
            "",
        )
        declared_name = name_line.split(":", 1)[1].strip() if ":" in name_line else ""
        if declared_name != skill_dir.name:
            errors.append(
                f"{skill_file}: frontmatter name {declared_name!r} does not match folder {skill_dir.name!r}"
            )

    readme = root / "README.md"
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        for skill_dir in skill_dirs:
            if f"`{skill_dir.name}`" not in readme_text:
                errors.append(f"README.md: missing published skill `{skill_dir.name}`")

        try:
            tracked_files = subprocess.check_output(
                ["git", "ls-files"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).splitlines()
        except (OSError, subprocess.CalledProcessError):
            tracked_files = []

        root_tokens = {
            ".agents": ".agents/skills/",
            "scripts": "scripts/check-skills.sh",
            "README.md": "README.md",
            "AGENTS.md": "AGENTS.md",
            "LICENSE": "LICENSE",
        }
        for top_level in sorted({path.split("/", 1)[0] for path in tracked_files}):
            token = root_tokens.get(top_level, top_level)
            if token not in readme_text:
                errors.append(
                    f"README.md: missing tracked top-level inventory entry for {top_level!r}"
                )
    else:
        errors.append("missing README.md")

link_sources = list(root.glob(".agents/skills/**/*.md")) + [
    path for path in (root / "README.md", root / "AGENTS.md") if path.is_file()
]

for path in link_sources:
    text = path.read_text(encoding="utf-8")
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

skill_ref_pattern = re.compile(r"^[a-z][a-z0-9]+(?:-[a-z0-9]+)+$")
skill_context_pattern = re.compile(
    r"\b(skill|skills|expected|compose|composes|pair|pairs|paired|routing|route|start with|use)\b",
    re.IGNORECASE,
)
known_non_skill_refs = {
    "clang-tidy",
    "frontier-gpt",
    "human",
    "local-small",
    "negative-adjacent",
    "playwright-cli",
    "run-code",
    "standard-agent",
    "state-save",
    "test-configuration",
    "test-fixtures",
    "test-use-options",
    "touch-events",
}

for path in link_sources:
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not skill_context_pattern.search(line):
            continue

        candidates = [
            match.group(1).strip()
            for pattern in (r"`([^`\n]+)`", r"\*\*([^*\n]+)\*\*")
            for match in re.finditer(pattern, line)
        ]

        for candidate in sorted(set(candidates)):
            if not skill_ref_pattern.match(candidate):
                continue
            if candidate in known_non_skill_refs:
                continue
            if candidate in skill_names:
                continue
            errors.append(
                f"{path}:{line_no}: possible unknown skill reference `{candidate}`"
            )

trigger_eval = (
    skills_dir
    / "agent-skill-generator"
    / "references"
    / "inventory-trigger-evals.md"
)
if not trigger_eval.is_file():
    errors.append(f"missing {trigger_eval}")

def read_required(path):
    if not path.is_file():
        errors.append(f"missing {path}")
        return ""
    return path.read_text(encoding="utf-8")

def require_contains(path, text, needle, label):
    if needle not in text:
        errors.append(f"{path}: missing story-family invariant: {label}")

def require_compact_contains(path, text, needle, label):
    compact_text = re.sub(r"\s+", " ", text)
    compact_needle = re.sub(r"\s+", " ", needle)
    if compact_needle not in compact_text:
        errors.append(f"{path}: missing story-family invariant: {label}")

def require_absent(path, text, needle, label):
    if needle in text:
        errors.append(f"{path}: forbidden story-family regression: {label}")

story_skill_paths = {
    "clarifier": skills_dir / "user-story-clarifier" / "SKILL.md",
    "scout": skills_dir / "story-repo-scout" / "SKILL.md",
    "planner": skills_dir / "story-implementation-planner" / "SKILL.md",
    "orchestrator": skills_dir / "story-implementation-orchestrator" / "SKILL.md",
}
story_texts = {
    name: read_required(path)
    for name, path in story_skill_paths.items()
}

for path in link_sources:
    text = path.read_text(encoding="utf-8")
    require_absent(path, text, "superpowers:", "legacy superpowers references")

clarifier_text = story_texts["clarifier"]
require_contains(
    story_skill_paths["clarifier"],
    clarifier_text,
    "Status: Split Candidate",
    "split packets keep top-level Split Candidate status",
)
require_contains(
    story_skill_paths["clarifier"],
    clarifier_text,
    "- Status: Ready | Needs Clarification | Blocked",
    "split slices carry their own readiness status",
)

orchestrator_text = story_texts["orchestrator"]
require_contains(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "Materialize the selected slice as the active story card before scouting",
    "selected split slices are materialized before scouting",
)
require_contains(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "Pass one materialized story card for the active slice",
    "scouting input is the active materialized slice, not the whole split set",
)
require_contains(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "`First Action` block present when",
    "orchestrator validates First Action conditionally",
)
require_compact_contains(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "optional for agent profiles, and absent for\n  `human`",
    "human plans omit First Action in orchestrator readiness",
)
require_contains(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "Default for repo-owned code changes: `project-core-dev`",
    "project-core-dev routing is conditional on code changes",
)
require_contains(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "Workflow overlay: `tester-mindset` when",
    "tester-mindset routing is conditional",
)
require_absent(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "- Always: `project-core-dev`",
    "unconditional project-core-dev routing",
)
require_absent(
    story_skill_paths["orchestrator"],
    orchestrator_text,
    "- Always: `tester-mindset`",
    "unconditional tester-mindset routing",
)

scout_text = story_texts["scout"]
require_contains(
    story_skill_paths["scout"],
    scout_text,
    "`None identified` when this output will feed",
    "Do Not Touch can explicitly report no boundary found",
)
require_compact_contains(
    story_skill_paths["scout"],
    scout_text,
    "Likely Unrelated / Do\nNot Touch` as `None identified`",
    "orchestrated packets preserve the None identified convention",
)

planner_text = story_texts["planner"]
require_contains(
    story_skill_paths["planner"],
    planner_text,
    "Required for `local-small`, optional for agent profiles",
    "planner treats First Action as executor-specific",
)
require_contains(
    story_skill_paths["planner"],
    planner_text,
    "omitted for `human`",
    "human plans omit First Action",
)
require_contains(
    story_skill_paths["planner"],
    planner_text,
    "repo-owned code changes",
    "planner routes project-core-dev only for repo-owned code changes",
)
require_contains(
    story_skill_paths["planner"],
    planner_text,
    "Add `tester-mindset` when",
    "planner routes tester-mindset conditionally",
)
require_absent(
    story_skill_paths["planner"],
    planner_text,
    "must hand off to `project-core-dev`",
    "unconditional project-core-dev planner handoff",
)

if errors:
    for error in errors:
        print(f"check-skills: {error}", file=sys.stderr)
    sys.exit(1)

print(f"check-skills: ok ({len(skill_dirs)} skills)")
PY
