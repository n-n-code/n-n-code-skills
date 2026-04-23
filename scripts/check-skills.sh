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

        keys = [
            line.split(":", 1)[0]
            for line in lines[1:end]
            if re.match(r"^[A-Za-z_-]+:", line)
        ]
        if keys != ["name", "description"]:
            errors.append(
                f"{skill_file}: frontmatter keys must be exactly name, description; got {keys}"
            )

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
    "negative-adjacent",
    "playwright-cli",
    "run-code",
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

if errors:
    for error in errors:
        print(f"check-skills: {error}", file=sys.stderr)
    sys.exit(1)

print(f"check-skills: ok ({len(skill_dirs)} skills)")
PY
