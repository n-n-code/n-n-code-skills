#!/usr/bin/env bash
# CMake-first scaffold. Adapt required scripts and optional build targets to the
# destination repo before installing it there. This skills repo has no such build.

set -euo pipefail

usage() {
    cat <<'EOF_USAGE'
Usage: bash scripts/run-release-checklist.sh [--build-dir DIR] [--help] [-- <cmake-configure-args...>]

Runs the automated portion of RELEASE_CHECKLIST.md up to, but not including,
manual release review. Requires CMake and CTest 3.20+ and the destination repo's helper
scripts. Build output is retained on success and failure for inspection; remove
only the exact task-owned temporary directory when it is no longer needed.
EOF_USAGE
}

die() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

note() {
    printf '==> %s\n' "$*"
}

run_cmd() {
    note "$*"
    "$@"
}

require_version() {
    local tool="$1" output major minor
    command -v "$tool" >/dev/null 2>&1 || die "Required tool unavailable: $tool"
    output="$("$tool" --version)" || die "Cannot query $tool version"
    if [[ "$output" =~ ^${tool}[[:space:]]version[[:space:]]([0-9]+)\.([0-9]+) ]]; then
        major="${BASH_REMATCH[1]}"
        minor="${BASH_REMATCH[2]}"
    else
        die "Cannot parse $tool version; version 3.20+ is required"
    fi
    (( 10#$major > 3 || (10#$major == 3 && 10#$minor >= 20) )) ||
        die "$tool 3.20+ is required; found $major.$minor"
}

build_dir=""
skipped_checks=0
declare -a extra_cmake_args=()

while [[ $# -gt 0 ]]; do
    case "$1" in
    --build-dir)
        [[ $# -ge 2 ]] || die "--build-dir requires a value"
        [[ -n "$2" && "$2" != --* ]] || die "--build-dir requires a directory"
        build_dir="$2"
        shift 2
        ;;
    --help)
        usage
        exit 0
        ;;
    --)
        shift
        extra_cmake_args=("$@")
        break
        ;;
    *)
        die "Unknown argument: $1"
        ;;
    esac
done

for tool in cmake ctest; do
    require_version "$tool"
done
for required in CMakeLists.txt scripts/check-release-hygiene.sh scripts/check-change-contracts.sh; do
    [[ -f "$required" ]] || die "Missing $required; run from the target repo or adapt this scaffold"
done

if [[ -z "$build_dir" ]]; then
    build_dir="$(mktemp -d "${TMPDIR:-/tmp}/project-release-build-XXXXXX")"
fi

report_exit() {
    local result=$?
    if (( result != 0 )); then
        printf 'Checks failed (exit %s); build output retained at: %s\n' "$result" "$build_dir" >&2
    fi
    return "$result"
}
trap report_exit EXIT

declare -a generator_args=()
if command -v ninja >/dev/null 2>&1 || command -v ninja-build >/dev/null 2>&1; then
    generator_args=(-G Ninja)
fi

note "Release checklist build directory: $build_dir"
run_cmd bash scripts/check-release-hygiene.sh
run_cmd bash scripts/check-change-contracts.sh
run_cmd cmake -S . -B "$build_dir" "${generator_args[@]}" -DCMAKE_BUILD_TYPE=Debug "${extra_cmake_args[@]}"
run_cmd cmake --build "$build_dir" --parallel
run_cmd ctest --test-dir "$build_dir" --output-on-failure --no-tests=error
if command -v valgrind >/dev/null 2>&1 && [[ -f scripts/run-valgrind.sh ]]; then
    run_cmd bash scripts/run-valgrind.sh "$build_dir"
else
    note "Skipping Valgrind: tool or repo helper unavailable"
    skipped_checks=$((skipped_checks + 1))
fi
if command -v clang-tidy >/dev/null 2>&1; then
    run_cmd cmake --build "$build_dir" --target clang-tidy
else
    note "Skipping clang-tidy because clang-tidy is not installed"
    skipped_checks=$((skipped_checks + 1))
fi
if command -v doxygen >/dev/null 2>&1; then
    run_cmd cmake --build "$build_dir" --target docs
else
    note "Skipping docs because doxygen is not installed"
    skipped_checks=$((skipped_checks + 1))
fi

cat <<EOF_SUMMARY

Executed pre-release checks passed. Optional checks skipped: $skipped_checks.
This does not establish that skipped checks or manual release review passed.

Build directory:
  $build_dir

Manual review items still remaining from RELEASE_CHECKLIST.md:
  - Review license, docs, workflows, and shipped assets for release accuracy.
  - Perform install validation.
  - Review any release notes or repository description before publishing.
EOF_SUMMARY
