#!/usr/bin/env python3
"""Exercise bundled resources; report unavailable optional runtimes as skips."""

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_skills  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RELEASE_EXAMPLE = ROOT / ".agents/skills/development-contract-process/references/run-release-checklist.example.sh"


def find_tool(name, override):
    """An explicit override must work; absent optional tools may be skipped."""
    if os.environ.get(override):
        path = Path(os.environ[override])
        if not path.is_file():
            raise RuntimeError(f"{override} does not identify a file: {path}")
        return str(path.resolve())
    candidates = [shutil.which(name)]
    if os.name == "nt":
        if name == "bash":
            git = shutil.which("git")
            if git:
                candidates.extend(str(Path(git).resolve().parent.parent / part / "bash.exe")
                                  for part in ("bin", "usr/bin"))
            candidates.append(str(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe"))
        elif name in {"cmake", "ctest"}:
            candidates.append(str(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "CMake/bin" / (name + ".exe")))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            if name == "bash" and os.name == "nt" and Path(candidate).parent.name.lower() == "system32":
                continue  # WSL needs different workspace and tool discovery semantics.
            return str(Path(candidate).resolve())
    return None


def write_text(path, text):
    with path.open("w", encoding="utf-8", newline="\n") as output:
        output.write(text)


def clean_environment():
    env = dict(os.environ)
    for name in ("BASH_ENV", "ENV", "CDPATH", "CTEST_NO_TESTS_ACTION"):
        env.pop(name, None)
    return env


def version_of(executable, name):
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10, check=True)
    match = re.search(r"^" + re.escape(name) + r" version (\d+)\.(\d+)", result.stdout)
    if not match:
        raise RuntimeError(f"Cannot determine {name} version")
    return tuple(int(part) for part in match.groups())


class ReleaseScaffoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bash = find_tool("bash", "SKILL_TEST_BASH")
        if not cls.bash:
            raise unittest.SkipTest("Bash unavailable; set SKILL_TEST_BASH to a compatible executable")

    def shell_path(self, path):
        if os.name != "nt":
            return str(path)
        result = subprocess.run(
            [self.bash, "-c", 'PATH="/usr/bin:/bin:$PATH" exec cygpath -u "$1"', "--", str(path)],
            capture_output=True, text=True, timeout=10, check=True,
            env=clean_environment(),
        )
        return result.stdout.strip()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-resource-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.assertEqual(self.root.parent, Path(tempfile.gettempdir()).resolve())
        self.bin = self.root / "bin"
        self.bin.mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "temp").mkdir()
        write_text(self.root / "CMakeLists.txt", "cmake_minimum_required(VERSION 3.20)\nproject(fixture NONE)\n")
        for name in ("check-release-hygiene.sh", "check-change-contracts.sh"):
            write_text(self.root / "scripts" / name, "#!/bin/bash\nexit 0\n")
        write_text(self.bin / "cmake", '''#!/bin/bash
if [[ "${1:-}" == --version ]]; then
    [[ "${VERSION_FAILURE:-}" == cmake ]] && exit 13
    printf 'cmake version %s\n' "${CMAKE_VERSION:-3.20.0}"
    exit 0
fi
printf '%s\\0' "$@" >> "$TRACE"
exit "${CMAKE_EXIT:-0}"
''')
        write_text(self.bin / "ctest", '''#!/bin/bash
if [[ "${1:-}" == --version ]]; then
    [[ "${VERSION_FAILURE:-}" == ctest ]] && exit 13
    printf 'ctest version %s\n' "${CTEST_VERSION:-3.20.0}"
    exit 0
fi
if [[ "${CTEST_EMPTY:-0}" == 1 ]]; then
    printf 'No tests were found!\n' >&2
    for arg in "$@"; do
        [[ "$arg" == --no-tests=error ]] && exit 8
    done
    exit 0
fi
exit "${CTEST_EXIT:-0}"
''')
        for path in self.bin.iterdir():
            path.chmod(0o755)
        self.trace = self.root / "argv trace"
        self.build = self.root / "build with spaces"
        self.build.mkdir()
        write_text(self.build / "existing.txt", "preserve")
        self.bin_arg = self.shell_path(self.bin)
        self.script_arg = self.shell_path(RELEASE_EXAMPLE)
        self.build_arg = self.shell_path(self.build)
        self.env = clean_environment()
        self.env.update(
            TRACE=self.shell_path(self.trace), TMPDIR=self.shell_path(self.root / "temp"),
            CMAKE_VERSION="3.20.0", CTEST_VERSION="3.20.0", CMAKE_EXIT="0", CTEST_EXIT="0",
            CTEST_EMPTY="0", VERSION_FAILURE="",
        )

    def run_example(self, args=None, **variables):
        env = dict(self.env)
        env.update(variables)
        return subprocess.run(
            [self.bash, "-c", 'PATH="$1:/usr/bin:/bin"; export PATH; exec bash "$2" "${@:3}"',
             "--", self.bin_arg, self.script_arg, *(args if args is not None else ["--build-dir", self.build_arg])],
            cwd=self.root, env=env, capture_output=True, text=True, timeout=15,
        )

    def assert_failure(self, result, code=None):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        if code is not None:
            self.assertEqual(result.returncode, code, result.stderr)
        self.assertNotIn("Executed pre-release checks passed", result.stdout)
        self.assertEqual((self.build / "existing.txt").read_text(), "preserve")

    def test_syntax_and_help_without_build_work(self):
        self.assertEqual(RELEASE_EXAMPLE.read_bytes().count(b"\r\n"), 0, "Shell resources must use LF for portable execution")
        result = subprocess.run([self.bash, "-n", self.script_arg], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_example(["--help"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.trace.exists())
        self.assertFalse(list((self.root / "temp").iterdir()))

    def test_missing_empty_and_unknown_arguments(self):
        for args in (["--build-dir"], ["--build-dir", ""], ["--build-dir", "--help"], ["--unknown"]):
            with self.subTest(args=args):
                self.assert_failure(self.run_example(args))
                self.assertFalse(self.trace.exists())

    def test_success_preserves_argument_boundaries_and_reports_skips(self):
        result = self.run_example(["--build-dir", self.build_arg, "--", "-DTEST_VALUE=a b"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Optional checks skipped: 3", result.stdout)
        argv = self.trace.read_bytes().split(b"\0")
        self.assertIn(b"-DTEST_VALUE=a b", argv)
        self.assertIn(b"--parallel", argv)

    def test_configure_test_and_helper_failures_preserve_exit_status(self):
        for variables, code in (({"CMAKE_EXIT": "7"}, 7), ({"CTEST_EXIT": "9"}, 9)):
            with self.subTest(variables=variables):
                result = self.run_example(**variables)
                self.assert_failure(result, code)
                self.assertIn(f"Checks failed (exit {code})", result.stderr)
        write_text(self.root / "scripts/check-release-hygiene.sh", "#!/bin/bash\nexit 6\n")
        self.assert_failure(self.run_example(), 6)

    def test_old_unknown_and_failed_version_checks_stop_before_work(self):
        for variables in (
            {"CMAKE_VERSION": "3.12.0"}, {"CTEST_VERSION": "3.19.8"},
            {"CMAKE_VERSION": "unknown"}, {"VERSION_FAILURE": "ctest"},
        ):
            with self.subTest(variables=variables):
                self.assert_failure(self.run_example(**variables))
                self.assertFalse(self.trace.exists())

    def test_supported_version_boundary_and_new_major(self):
        for version in ("3.20.0", "4.0.0"):
            with self.subTest(version=version):
                result = self.run_example(CMAKE_VERSION=version, CTEST_VERSION=version)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_empty_test_selection_is_failure(self):
        result = self.run_example(CTEST_EMPTY="1")
        self.assert_failure(result, 8)


class RealCTestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cmake = find_tool("cmake", "SKILL_TEST_CMAKE")
        cls.ctest = find_tool("ctest", "SKILL_TEST_CTEST")
        if not cls.cmake or not cls.ctest:
            raise unittest.SkipTest("real CMake/CTest unavailable; stub checks do not prove real-tool behavior")
        if min(version_of(cls.cmake, "cmake"), version_of(cls.ctest, "ctest")) < (3, 20):
            raise unittest.SkipTest("real CMake and CTest 3.20+ required")

    def run_ctest(self, definitions):
        with tempfile.TemporaryDirectory(prefix="skill-ctest-") as temporary:
            root = Path(temporary).resolve()
            self.assertEqual(root.parent, Path(tempfile.gettempdir()).resolve())
            write_text(root / "CTestTestfile.cmake", definitions)
            return subprocess.run(
                [self.ctest, "--test-dir", str(root), "--output-on-failure", "--no-tests=error"],
                env=clean_environment(), capture_output=True, text=True, timeout=20,
            )

    def test_real_test_discovery_pass_and_failure(self):
        python = Path(sys.executable).as_posix().replace('"', '\\"')
        for code, expected in ((0, 0), (7, 8)):
            with self.subTest(exit_code=code):
                result = self.run_ctest(f'add_test(example "{python}" "-c" "raise SystemExit({code})")\n')
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_real_empty_test_selection_fails(self):
        result = self.run_ctest("# Intentionally empty test inventory.\n")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless(importlib.util.find_spec("yaml"), "PyYAML unavailable; independent parser comparison not run")
class YamlReferenceTests(unittest.TestCase):
    def test_accepted_scalars_match_reference_decoder(self):
        import yaml
        for value in ("Review C# and C++ code.", "'Review the user''s code.'", '"true"',
                      "'alpha:\tbeta'", r'"alpha:\tbeta"', "Review café and 日本語."):
            with self.subTest(value=value):
                parsed = yaml.safe_load("name: example\ndescription: " + value + "\n")
                self.assertEqual(check_skills.parse_frontmatter_value(value), parsed["description"])

    def test_invalid_source_probes_fail_both_readers(self):
        import yaml
        for value in ("alpha\x00beta", "alpha:\tbeta"):
            with self.subTest(value=ascii(value)):
                with self.assertRaises(yaml.YAMLError):
                    yaml.safe_load("name: example\ndescription: " + value + "\n")
                _, errors = check_skills.check_frontmatter_lines(
                    "example/SKILL.md", ["name: example", "description: " + value]
                )
                self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
