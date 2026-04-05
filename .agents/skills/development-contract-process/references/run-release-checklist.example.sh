#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF_USAGE'
Usage: bash scripts/run-release-checklist.sh [--build-dir DIR] [--help] [-- <cmake-configure-args...>]

Runs the automated portion of RELEASE_CHECKLIST.md up to, but not including,
manual release review.
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

run_build_target() {
    shift
    "$@"
}

build_dir=""
declare -a extra_cmake_args=()

while [[ $# -gt 0 ]]; do
    case "$1" in
    --build-dir)
        [[ $# -ge 2 ]] || die "--build-dir requires a value"
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

if [[ -z "$build_dir" ]]; then
    build_dir="$(mktemp -d /tmp/project-release-build-XXXXXX)"
fi

declare -a generator_args=()
if command -v ninja >/dev/null 2>&1 || command -v ninja-build >/dev/null 2>&1; then
    generator_args=(-G Ninja)
fi

note "Release checklist build directory: $build_dir"
run_cmd bash scripts/check-release-hygiene.sh
run_cmd bash scripts/check-change-contracts.sh
run_cmd cmake -S . -B "$build_dir" "${generator_args[@]}" -DCMAKE_BUILD_TYPE=Debug "${extra_cmake_args[@]}"
run_build_target "$build_dir" cmake --build "$build_dir" -j"$(nproc)"
run_cmd ctest --test-dir "$build_dir" --output-on-failure
if command -v valgrind >/dev/null 2>&1; then
    run_cmd bash scripts/run-valgrind.sh "$build_dir"
else
    note "Skipping Valgrind because valgrind is not installed"
fi
if command -v clang-tidy >/dev/null 2>&1; then
    run_build_target "$build_dir" cmake --build "$build_dir" --target clang-tidy
else
    note "Skipping clang-tidy because clang-tidy is not installed"
fi
if command -v doxygen >/dev/null 2>&1; then
    run_build_target "$build_dir" cmake --build "$build_dir" --target docs
else
    note "Skipping docs because doxygen is not installed"
fi

cat <<EOF_SUMMARY

Automated pre-release checks passed.

Build directory:
  $build_dir

Manual review items still remaining from RELEASE_CHECKLIST.md:
  - Review license, docs, workflows, and shipped assets for release accuracy.
  - Perform install validation.
  - Review any release notes or repository description before publishing.
EOF_SUMMARY
