#!/usr/bin/env python3
"""Regression checks for the bounded-delegation fixture and grading contracts."""

import ast
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
from types import SimpleNamespace
import unittest
from unittest import mock

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/bounded-delegation/scripts/pilot_cases.py"
SPEC = importlib.util.spec_from_file_location("bounded_pilot_cases", SCRIPT)
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


LABEL_TESTS = textwrap.dedent('''\
    import unittest
    from app.labels import normalize_labels
    FIXTURE_RUN = RUN_ID
    print("test module diagnostic")

    class LabelTests(unittest.TestCase):
        def test_normalization(self):
            self.assertEqual(normalize_labels(" B , a, B, ,\\t"), ["b", "a"])
        def test_unicode(self):
            self.assertEqual(normalize_labels("Straße,STRASSE"), ["strasse"])
        def test_limit(self):
            self.assertEqual(normalize_labels("a,b,c", 1), ["a"])
        def test_default_limit(self):
            self.assertEqual(normalize_labels("a,b,c,d,e,f"), list("abcde"))
        def test_bool(self):
            with self.assertRaises(TypeError):
                normalize_labels("a", True)
        def test_lower_bound(self):
            with self.assertRaises(ValueError):
                normalize_labels("a", 0)
        def test_upper_bound(self):
            with self.assertRaises(ValueError):
                normalize_labels("a", 21)
        def test_value_type(self):
            with self.assertRaises(TypeError):
                normalize_labels(None)
        def test_noninteger(self):
            with self.assertRaises(TypeError):
                normalize_labels("a", 1.5)
        def test_empty(self):
            print("test execution diagnostic")
            self.assertEqual(normalize_labels(""), [])
''')

CONFIG = textwrap.dedent('''\
    from dataclasses import dataclass
    from typing import Literal
    FIXTURE_RUN = RUN_ID
    print("config module diagnostic")
    Transport = Literal["http", "https"]
    @dataclass(frozen=True)
    class MirrorConfig:
        mirror_id: str
        endpoint: str
        transport: Transport = "https"
        enabled: bool = True
        retry_limit: int = 3
''')

PROFILES = [
    {"mirror_id": "primary", "endpoint": "https://primary.example.test/assets",
     "transport": "https", "enabled": True, "retry_limit": 3},
    {"mirror_id": "staging", "endpoint": "https://staging.example.test/assets",
     "transport": "https", "enabled": False, "retry_limit": 1},
    {"mirror_id": "loopback", "endpoint": "http://127.0.0.1:8080/assets",
     "transport": "http", "enabled": True, "retry_limit": 0},
]


class PilotTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="skill-pilot-test-")
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(temporary.name).resolve()
        self.assertEqual(self.scratch.parent, Path(tempfile.gettempdir()).resolve())
        self.root = self.scratch / "fixtures"

    def prepare(self):
        self.run_id = pilot.prepare(self.root)["run_id"]

    def write_json(self, path, value):
        pilot.write(path, json.dumps(value))

    def finish_readers(self):
        wanted = {"service-014": "retention_days", "service-067": "owner",
                  "service-114": "shards", "service-173": "retention_days", "service-209": "owner"}
        for arm in pilot.ARMS:
            worker = self.root / "p1" / arm
            records = []
            service = None
            for line, text in enumerate((worker / "source/operations.md").read_text(encoding="utf-8").splitlines(), 1):
                if text.startswith("## "):
                    service = text[3:]
                prefix = f"Current {wanted.get(service)}: "
                if service in wanted and text.startswith(prefix):
                    records.append({"service": service, "field": wanted[service], "value": text[len(prefix):],
                                    "path": "source/operations.md", "line": line, "quote": text})
            self.write_json(worker / "answer.json", {"run_id": self.run_id, "records": records})
            worker = self.root / "p2" / arm
            calls = []
            for group in ("readers", "writers"):
                for path in (worker / "app" / group).rglob("*.py"):
                    if "archived" in path.parts or path.name.endswith("_test.py"):
                        continue
                    tree = ast.parse(path.read_text(encoding="utf-8"))
                    for function in (node for node in tree.body if isinstance(node, ast.FunctionDef)):
                        for call in (node for node in ast.walk(function) if isinstance(node, ast.Call)):
                            if (isinstance(call.func, ast.Name) and call.func.id == "RetryPolicy"
                                    and any(keyword.arg == "attempts" and isinstance(keyword.value, ast.Constant)
                                            and keyword.value.value == 4 for keyword in call.keywords)):
                                calls.append({"path": path.relative_to(worker).as_posix(),
                                              "line": call.lineno, "function": function.name})
            self.write_json(worker / "answer.json", {"run_id": self.run_id, "calls": calls})

    def finish_generators(self):
        for arm in pilot.ARMS:
            for case, name, source in (("p3", "test_labels.py", LABEL_TESTS), ("p4", "mirror_config.py", CONFIG)):
                source = source.replace("RUN_ID", repr(self.run_id))
                if arm == "candidate":
                    source = source.replace("FIXTURE_RUN = ", "FIXTURE_RUN: str = ")
                pilot.write(self.root / case / arm / "generated" / name, source)
            self.write_json(self.root / "p4" / arm / "generated/profiles.json",
                            {"run_id": self.run_id, "profiles": PROFILES})

    def results(self):
        result = pilot.grade(self.root)
        self.assertEqual(len(result["results"]), 8)
        return {(item["case"], item["arm"]): item for item in result["results"]}

    def cli(self, *arguments):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, arguments)],
                                capture_output=True, text=True, timeout=60, check=False)
        return result, json.loads(result.stdout)

    def test_completed_pilots_pass_cli_with_annotations_and_diagnostics(self):
        self.prepare()
        self.finish_readers()
        self.finish_generators()
        process, result = self.cli("grader", "--root", self.root)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertTrue(result["passed"])
        self.assertEqual(len(result["results"]), 8)
        self.assertTrue(all(item["passed"] for item in result["results"]))
        for item in result["results"]:
            if item["case"] == "p3":
                self.assertEqual(item["tests_discovered"], 10)
                self.assertEqual(set(item["mutants_killed"]), set(pilot.MUTATIONS))
                self.assertEqual(item["mutants_survived"], [])

    def test_runner_stdout_is_protocol_and_diagnostics_are_stderr(self):
        self.prepare()
        self.finish_generators()
        test_worker = self.root / "p3/candidate"
        config_worker = self.root / "p4/candidate/generated"
        for program, arguments, diagnostics in (
            (pilot.TEST_RUNNER, [test_worker], ["test module diagnostic", "test execution diagnostic"]),
            (pilot.CONFIG_RUNNER, [config_worker / "mirror_config.py", config_worker / "profiles.json"],
             ["config module diagnostic"]),
        ):
            with self.subTest(diagnostics=diagnostics):
                result = subprocess.run([sys.executable, "-I", "-B", "-c", program, *map(str, arguments)],
                                        capture_output=True, text=True, timeout=15, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIsInstance(json.loads(result.stdout), dict)
                for diagnostic in diagnostics:
                    self.assertIn(diagnostic, result.stderr)
                    self.assertNotIn(diagnostic, result.stdout)

    def test_run_constant_accepts_plain_and_annotated_literals(self):
        run_id = "a" * 32
        path = self.scratch / "module.py"
        for declaration in (f"FIXTURE_RUN = {run_id!r}\n", f"FIXTURE_RUN: str = {run_id!r}\n"):
            with self.subTest(declaration=declaration):
                pilot.write(path, declaration)
                pilot.check_python(path, run_id, set())

    def test_run_constant_rejects_missing_stale_duplicate_and_dynamic_values(self):
        run_id = "a" * 32
        valid = f"FIXTURE_RUN = {run_id!r}\n"
        annotated = f"FIXTURE_RUN: str = {run_id!r}\n"
        declarations = {
            "missing": "other = 1\n", "stale": "FIXTURE_RUN = 'old'\n",
            "annotation_only": "FIXTURE_RUN: str\n", "dynamic": "FIXTURE_RUN = make_id()\n",
            "duplicate": valid + valid, "mixed": valid + annotated,
            "annotated_duplicate": annotated + annotated,
            "dynamic_reassignment": valid + "FIXTURE_RUN = make_id()\n",
            "annotated_dynamic_reassignment": valid + "FIXTURE_RUN: str = make_id()\n",
            "augmented_reassignment": valid + "FIXTURE_RUN += '_changed'\n",
            "unpacked_reassignment": valid + "FIXTURE_RUN, other = ('old', 1)\n",
        }
        path = self.scratch / "module.py"
        for name, source in declarations.items():
            with self.subTest(name=name):
                pilot.write(path, source)
                with self.assertRaisesRegex(ValueError, "FIXTURE_RUN"):
                    pilot.check_python(path, run_id, set())

    def test_prepare_refuses_relative_and_existing_destinations(self):
        with self.assertRaisesRegex(ValueError, "absolute"):
            pilot.prepare(Path("relative-fixture"))
        self.prepare()
        manifest = (self.root / "manifest.json").read_bytes()
        with self.assertRaises(FileExistsError):
            pilot.prepare(self.root)
        self.assertEqual((self.root / "manifest.json").read_bytes(), manifest)

    def test_invalid_manifest_is_invocation_error(self):
        self.prepare()
        self.write_json(self.root / "manifest.json", {"format": 1, "run_id": "old"})
        process, result = self.cli("grader", "--root", self.root)
        self.assertEqual(process.returncode, 2)
        self.assertFalse(result["passed"])
        self.assertIn("Invalid fixture manifest", result["error"])

    def test_missing_arm_preserves_valid_peer_and_partial_cli_report(self):
        self.prepare()
        self.finish_readers()
        (self.root / "p1/candidate").rename(self.scratch / "unused-arm")
        process, result = self.cli("grader", "--root", self.root)
        self.assertEqual(process.returncode, 1)
        self.assertEqual(len(result["results"]), 8)
        arms = {(item["case"], item["arm"]): item for item in result["results"]}
        self.assertTrue(arms["p1", "baseline"]["passed"])
        self.assertFalse(arms["p1", "candidate"]["passed"])
        self.assertTrue(arms["p2", "candidate"]["passed"])

    def test_missing_case_preserves_other_cases(self):
        self.prepare()
        self.finish_readers()
        (self.root / "p1").rename(self.scratch / "unused-case")
        results = self.results()
        self.assertFalse(results["p1", "baseline"]["passed"])
        self.assertFalse(results["p1", "candidate"]["passed"])
        self.assertTrue(results["p2", "baseline"]["passed"])

    def test_changed_or_missing_input_fails_only_affected_arm(self):
        self.prepare()
        self.finish_readers()
        source = self.root / "p1/candidate/source/operations.md"
        original = source.read_bytes()
        for changed in (original + b"extra\n", None):
            with self.subTest(changed=changed is not None):
                if changed is None:
                    source.unlink()
                else:
                    source.write_bytes(changed)
                results = self.results()
                self.assertTrue(results["p1", "baseline"]["passed"])
                self.assertFalse(results["p1", "candidate"]["passed"])

    def test_bad_reader_outputs_fail_without_hiding_peer(self):
        self.prepare()
        self.finish_readers()
        path = self.root / "p1/candidate/answer.json"
        good = path.read_text(encoding="utf-8")
        stale = json.loads(good)
        stale["run_id"] = "old"
        bad_line = json.loads(good)
        bad_line["records"][0]["line"] = True
        duplicate = good.replace('"run_id":', '"run_id": "duplicate", "run_id":', 1)
        for name, content in (("malformed", "{"), ("stale", json.dumps(stale)),
                              ("line_type", json.dumps(bad_line)), ("duplicate_key", duplicate),
                              ("missing", None)):
            with self.subTest(name=name):
                if content is None:
                    path.unlink()
                else:
                    pilot.write(path, content)
                results = self.results()
                self.assertFalse(results["p1", "candidate"]["passed"])
                self.assertTrue(results["p1", "baseline"]["passed"])

    def test_unexpected_output_rejected_and_bytecode_reported(self):
        self.prepare()
        self.finish_readers()
        worker = self.root / "p1/candidate"
        pilot.write(worker / "__pycache__/ignored.pyc", "not imported")
        result = self.results()["p1", "candidate"]
        self.assertTrue(result["passed"])
        self.assertEqual(result["ignored_bytecode_files"], ["__pycache__/ignored.pyc"])
        pilot.write(worker / "extra.txt", "unexpected")
        result = self.results()["p1", "candidate"]
        self.assertFalse(result["passed"])
        self.assertIn("Unexpected output file", result["error"])

    def test_weak_suite_does_not_pass_mutation_checks(self):
        self.prepare()
        worker = self.root / "p3/candidate"
        methods = "".join(f"    def test_{number}(self): self.assertTrue(True)\n" for number in range(5))
        pilot.write(worker / "generated/test_labels.py",
                    f"import unittest\nFIXTURE_RUN = {self.run_id!r}\nclass Tests(unittest.TestCase):\n" + methods)
        result = pilot.grade_tests(worker, self.run_id)
        self.assertFalse(result["passed"])
        self.assertEqual(set(result["mutants_survived"]), set(pilot.MUTATIONS))

    def test_empty_failing_and_skipped_suites_are_rejected(self):
        self.prepare()
        worker = self.root / "p3/candidate"
        for name, suffix in (("empty", ""), ("failure", "    def test_fail(self): self.fail('failed')\n"),
                             ("skip", "    @unittest.skip('skip')\n    def test_skip(self): pass\n"),
                             ("expected_failure", "    @unittest.expectedFailure\n    def test_fail(self): self.fail()\n")):
            with self.subTest(name=name):
                methods = "".join(f"    def test_{number}(self): self.assertTrue(True)\n" for number in range(5))
                source = f"import unittest\nFIXTURE_RUN = {self.run_id!r}\n"
                if name != "empty":
                    source += "class Tests(unittest.TestCase):\n" + methods + suffix
                pilot.write(worker / "generated/test_labels.py", source)
                with self.assertRaisesRegex(ValueError, "Suite must discover"):
                    pilot.grade_tests(worker, self.run_id)

    def test_mutable_scaffold_is_rejected(self):
        self.prepare()
        self.finish_generators()
        worker = self.root / "p4/candidate"
        path = worker / "generated/mirror_config.py"
        pilot.write(path, path.read_text(encoding="utf-8").replace("frozen=True", "frozen=False"))
        with self.assertRaisesRegex(ValueError, "MirrorConfig is mutable"):
            pilot.grade_config(worker, self.run_id)

    def test_malformed_runner_protocol_and_process_failure_are_rejected(self):
        for program, message in (("print('not json')", "valid result object"),
                                 ("raise RuntimeError('runner failed')", "runner failed")):
            with self.subTest(program=program), self.assertRaisesRegex(ValueError, message):
                pilot.run_python(program)

    def test_timeout_is_a_failed_arm_not_an_aborted_report(self):
        self.prepare()
        self.finish_readers()
        self.finish_generators()
        with mock.patch.object(pilot, "run_python", side_effect=subprocess.TimeoutExpired("python", 15)):
            results = self.results()
        self.assertTrue(results["p1", "baseline"]["passed"])
        self.assertTrue(results["p2", "candidate"]["passed"])
        for case in ("p3", "p4"):
            for arm in pilot.ARMS:
                self.assertFalse(results[case, arm]["passed"])
                self.assertIn("TimeoutExpired", results[case, arm]["error"])

    def test_samefile_aliases_are_rejected_for_both_arms(self):
        self.prepare()
        self.finish_readers()
        original = Path.samefile

        def samefile(path, other):
            if path.parent == self.root / "p1":
                return True
            return original(path, other)

        with mock.patch.object(Path, "samefile", autospec=True, side_effect=samefile):
            results = self.results()
        for arm in pilot.ARMS:
            self.assertFalse(results["p1", arm]["passed"])
            self.assertIn("distinct fixture directories", results["p1", arm]["error"])
            self.assertTrue(results["p2", arm]["passed"])

    def test_windows_reparse_attribute_is_rejected_without_following(self):
        info = SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
        with mock.patch.object(pilot.stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400, create=True), \
                mock.patch.object(Path, "lstat", return_value=info):
            with self.assertRaisesRegex(ValueError, "Linked path"):
                pilot.check_plain_directory(self.root)

    def create_link(self, path, target, junction):
        if junction:
            powershell = shutil.which("powershell") or shutil.which("pwsh")
            if os.name != "nt" or not powershell:
                self.skipTest("Windows junction creation requires Windows and PowerShell")
            environment = dict(os.environ, PILOT_TEST_LINK=str(path), PILOT_TEST_TARGET=str(target))
            result = subprocess.run(
                [powershell, "-NoProfile", "-NonInteractive", "-Command",
                 "New-Item -ItemType Junction -Path $env:PILOT_TEST_LINK -Target $env:PILOT_TEST_TARGET | Out-Null"],
                capture_output=True, text=True, timeout=15, check=False, env=environment,
            )
            if result.returncode:
                self.skipTest("Windows junction unavailable: " + result.stderr.strip())
        else:
            try:
                path.symlink_to(target, target_is_directory=target.is_dir())
            except OSError as error:
                self.skipTest(f"True symlink creation unavailable: {error}")

    def check_link_levels(self, junction):
        self.prepare()
        self.finish_readers()
        levels = {"root": self.root, "case": self.root / "p1", "arm": self.root / "p1/candidate",
                  "descendant": self.root / "p1/candidate/source", "manifest": self.root / "manifest.json"}
        for level, path in levels.items():
            if junction and level == "manifest":
                continue  # Junctions represent directories; the symlink case covers the manifest.
            with self.subTest(level=level):
                saved = self.scratch / f"saved-{level}"
                self.assertTrue(path.is_relative_to(self.scratch))
                self.assertTrue(saved.is_relative_to(self.scratch))
                path.rename(saved)
                try:
                    target = self.root / "p1/baseline" if level == "arm" else saved
                    self.create_link(path, target, junction)
                    self.assertTrue(path.samefile(target))
                    if level in ("root", "manifest"):
                        with self.assertRaisesRegex(ValueError, "Linked path"):
                            pilot.grade(self.root)
                    else:
                        results = self.results()
                        self.assertFalse(results["p1", "candidate"]["passed"])
                        self.assertIn("Linked path", results["p1", "candidate"]["error"])
                        self.assertEqual(results["p1", "baseline"]["passed"], level != "case")
                        self.assertTrue(results["p2", "baseline"]["passed"])
                finally:
                    if path.is_symlink():
                        path.unlink()
                    elif junction and path.exists():
                        path.rmdir()  # Remove only the junction, never its target tree.
                    saved.rename(path)

    def test_true_symlinks_at_fixture_boundaries_are_rejected(self):
        self.check_link_levels(junction=False)

    @unittest.skipUnless(os.name == "nt", "Real Windows junction checks require Windows")
    def test_real_junctions_at_fixture_boundaries_are_rejected(self):
        self.check_link_levels(junction=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
