#!/usr/bin/env python3
"""Prepare paired worker inputs and independently grade bounded-delegation pilots."""

import argparse
import ast
from collections.abc import Iterator
import json
from os import stat_result
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import textwrap
import uuid

sys.dont_write_bytecode = True
ARMS = ("baseline", "candidate")
CASES = ("p1", "p2", "p3", "p4")
OUTPUTS = {
    "p1": {"answer.json"}, "p2": {"answer.json"},
    "p3": {"generated/test_labels.py"},
    "p4": {"generated/mirror_config.py", "generated/profiles.json"},
}


def clean(text):
    return textwrap.dedent(text).lstrip("\n")


LABELS = clean('''
    def normalize_labels(value, limit=5):
        """Normalize comma-separated labels, retaining first occurrence order."""
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        if type(limit) is not int:
            raise TypeError("limit must be an integer")
        if not 1 <= limit <= 20:
            raise ValueError("limit must be between 1 and 20")
        result = []
        for raw in value.split(","):
            label = raw.strip().casefold()
            if label and label not in result:
                result.append(label)
        return result[:limit]
''')

# These mutations are grader-only. Every mutant remains a valid implementation
# with the same API and changes one behavior described in the worker's contract.
MUTATIONS = {
    "whitespace": ("raw.strip().casefold()", "raw.casefold()"),
    "unicode_casefold": ("raw.strip().casefold()", "raw.strip().lower()"),
    "duplicates": ("if label and label not in result:", "if label:"),
    "empty_segments": ("if label and label not in result:", "if label not in result:"),
    "first_seen_order": ("return result[:limit]", "return sorted(result)[:limit]"),
    "limit": ("return result[:limit]", "return result[:limit + 1]"),
    "boolean_limit": ("if type(limit) is not int:", "if not isinstance(limit, int):"),
    "upper_bound": ("if not 1 <= limit <= 20:", "if not 1 <= limit <= 21:"),
    "lower_bound": ("if not 1 <= limit <= 20:", "if not 0 <= limit <= 20:"),
    "value_type": ("raise TypeError(\"value must be a string\")", "return []"),
}


def inputs(case, run_id):
    """Return worker files and an oracle that is never written into worker dirs."""
    preamble = (
        f"Pilot {case.upper()}; fixture run {run_id}.\n"
        "Work only inside this directory. Preserve every supplied input file.\n"
        "Do not read sibling directories, the preparation script, or grader code.\n"
        "Use only the Python standard library; no installs or network access.\n"
    )
    if case == "p1":
        lines = ["# Service operating ledger", "", "Only Current fields are active. Historical notes are not active settings.", ""]
        targets = {14: "retention_days", 67: "owner", 114: "shards", 173: "retention_days", 209: "owner"}
        oracle = []
        for number in range(240):
            service = f"service-{number:03}"
            values = {"retention_days": str(7 + (number * 13) % 55),
                      "owner": ("Cedar", "Quartz", "Atlas", "Ember", "Tidal")[number % 5],
                      "shards": str(1 + (number * 7) % 16)}
            lines.extend([f"## {service}", "", f"Region: zone-{number % 9}",
                          f"Historical note: retention_days was {90 + number % 9}; owner was Legacy-{number % 4}."])
            for field, value in values.items():
                quote = f"Current {field}: {value}"
                lines.append(quote)
                if targets.get(number) == field:
                    oracle.append({"service": service, "field": field, "value": value,
                                   "path": "source/operations.md", "line": len(lines), "quote": quote})
            lines.extend([f"Maintenance note: review batch {number // 12}; keep regional failover notes with the owner.", ""])
        requests = ", ".join(f"service-{n:03} {field}" for n, field in targets.items())
        task = preamble + clean(f'''
            Read source/operations.md and extract these five active facts: {requests}.
            Write only answer.json, a JSON object with run_id equal to {run_id!r}
            and records containing one object per requested fact. Each record must have
            exactly service, field, value (a string), path (relative, forward slashes),
            line (1-based integer), and quote (the exact complete source line).
            Cite the Current field itself, not its heading or historical note.
            Return no additional records. Record order does not matter.
        ''')
        return {"task.txt": task, "source/operations.md": "\n".join(lines) + "\n"}, oracle

    if case == "p2":
        files = {}
        oracle = []
        for group in ("readers", "writers"):
            for number in range(9):
                path = f"app/{group}/channel_{number}.py"
                attempts = 4 if (number + (group == "writers")) % 3 == 0 else 2
                function = f"open_{group}_{number}"
                content = clean(f'''
                    """Channel adapter; documentation example: RetryPolicy(attempts=4)."""
                    from app.policy import RetryPolicy


                    def {function}():
                        # Old proposal: RetryPolicy(attempts=4); comments are not calls.
                        policy = RetryPolicy(
                            attempts={attempts},
                            pause_seconds={number + 1},
                        )
                        return policy


                    def diagnostic_policy():
                        return RetryPolicy(attempts=2, pause_seconds=0)


                    def dynamic_policy(attempts=4):
                        return RetryPolicy(attempts=attempts, pause_seconds=1)
                ''')
                files[path] = content
                if attempts == 4:
                    oracle.append({"path": path, "line": 7, "function": function})
        excluded = "def sample():\n    return RetryPolicy(attempts=4, pause_seconds=1)\n"
        files.update({"app/readers/channel_test.py": excluded,
                      "app/writers/archived/legacy.py": excluded,
                      "examples/demo.py": excluded, "tests/test_policy.py": excluded,
                      "app/policy.py": "class RetryPolicy:\n    pass\n"})
        files["task.txt"] = preamble + clean(f'''
            Inventory executable calls to the name RetryPolicy with the literal keyword
            attempts=4. Search app/readers/ and app/writers/ recursively, excluding
            directories named archived and filenames ending _test.py. Ignore comments,
            docstrings, nonliteral arguments, other paths, and other attempts values.
            Write only answer.json: {{"run_id": "{run_id}", "calls": [...]}}.
            Every call entry has exactly path (relative forward slashes), line (the
            1-based line where the RetryPolicy call begins), and function (the enclosing
            function name). Include all and only matching calls; order does not matter.
        ''')
        return files, oracle

    if case == "p3":
        return {
            "task.txt": preamble + clean(f'''
                Create only generated/test_labels.py, a Python unittest suite for
                app.labels.normalize_labels(value, limit=5). Follow the style in
                tests/test_counter.py. Read behavior.md as the authority for behavior.
                Include a module constant FIXTURE_RUN = "{run_id}".
                Use at least five independently discovered test methods; no skips,
                expected failures, source introspection, mocks, or implementation edits.
                Import only unittest and app.labels. Exercise the real function.
                Use python -B if running tests, so no bytecode files are created.
            '''),
            "behavior.md": clean('''
                # Label contract

                normalize_labels(value, limit=5) returns a list of strings.
                value must be a str (including subclasses); otherwise raise TypeError.
                limit must have exact type int: bool and all non-int values raise TypeError.
                Valid limits are 1 through 20 inclusive; other integers raise ValueError.
                Split value on commas. Strip surrounding whitespace from every segment,
                then apply Unicode str.casefold (not merely lower). Discard empty labels.
                Deduplicate after normalization while preserving first occurrence order.
                Return at most limit unique labels; the default limit is five.
                Empty or whitespace-only input returns an empty list. Inputs are not mutated.
                Error message wording is not part of this contract.
            '''),
            "app/__init__.py": "", "app/labels.py": LABELS,
            "tests/test_counter.py": clean('''
                import unittest


                class CounterTests(unittest.TestCase):
                    def test_increment(self):
                        self.assertEqual(1 + 1, 2)

                    def test_reject_non_integer(self):
                        with self.assertRaises(TypeError):
                            1 + "one"


                if __name__ == "__main__":
                    unittest.main()
            '''),
        }, None

    if case == "p4":
        return {
            "task.txt": preamble + clean(f'''
                Create only generated/mirror_config.py and generated/profiles.json.
                Implement the exact data/type scaffold in spec.md, following the pattern
                in reference/cache_config.py. Use Python standard library only. Do not
                add validation, network code, constructors, or unrelated helpers.
                In the Python module set FIXTURE_RUN = "{run_id}". In the JSON root set
                run_id to "{run_id}". Preserve all supplied inputs.
            '''),
            "reference/cache_config.py": clean('''
                from dataclasses import dataclass
                from typing import Literal

                CacheMode = Literal["memory", "disk"]


                @dataclass(frozen=True)
                class CacheConfig:
                    name: str
                    mode: CacheMode = "memory"
                    enabled: bool = True
            '''),
            "spec.md": clean('''
                # Mirror scaffold

                mirror_config.py exports Transport = Literal["http", "https"] and a
                frozen dataclass MirrorConfig with these fields in exactly this order:
                mirror_id: str (required), endpoint: str (required),
                transport: Transport = "https", enabled: bool = True,
                retry_limit: int = 3. Keep the normal dataclass-generated constructor,
                equality, and repr. Use no custom methods. Field annotations must resolve
                to those types. Do not make the fields keyword-only or add slots.

                profiles.json is an object with exactly run_id and profiles. profiles
                contains the following objects, in this order, with exactly the five
                MirrorConfig field names in every object, and explicit values for defaults:

                - mirror_id "primary", endpoint "https://primary.example.test/assets",
                  transport "https", enabled true, retry_limit 3.
                - mirror_id "staging", endpoint "https://staging.example.test/assets",
                  transport "https", enabled false, retry_limit 1.
                - mirror_id "loopback", endpoint "http://127.0.0.1:8080/assets",
                  transport "http", enabled true, retry_limit 0.
            '''),
        }, None
    raise ValueError(f"Unknown case: {case}")


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def prepare(destination):
    if not destination.is_absolute():
        raise ValueError("--dest must be an absolute path")
    # mkdir is deliberately exclusive; no delete or reuse of a previous run.
    destination.mkdir(parents=True, exist_ok=False)
    run_id = uuid.uuid4().hex
    write(destination / "manifest.json", json.dumps({"format": 1, "run_id": run_id}) + "\n")
    for case in CASES:
        files, _ = inputs(case, run_id)
        for arm in ARMS:
            for name, content in files.items():
                write(destination / case / arm / name, content)
    return {"prepared": str(destination), "run_id": run_id, "cases": list(CASES), "arms": list(ARMS)}


def load_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def grade_read(worker, run_id, key, expected):
    answer = load_json(worker / "answer.json")
    if not isinstance(answer, dict) or set(answer) != {"run_id", key} or answer["run_id"] != run_id:
        raise ValueError("Wrong answer schema or stale run_id")
    records = answer[key]
    if not isinstance(records, list) or len(records) != len(expected):
        raise ValueError("Missing, duplicate, or extra records")
    if any(not isinstance(record, dict) or type(record.get("line")) is not int for record in records):
        raise ValueError("Records must be objects with integer source lines")
    canonical = lambda record: json.dumps(record, sort_keys=True)
    if sorted(map(canonical, records)) != sorted(map(canonical, expected)):
        raise ValueError("Facts, paths, locations, or inventory do not match source evidence")
    for record in records:
        lines = (worker / record["path"]).read_text(encoding="utf-8").splitlines()
        if not 1 <= record["line"] <= len(lines):
            raise ValueError("Source location is out of range")
        if "quote" in record and lines[record["line"] - 1] != record["quote"]:
            raise ValueError("Quote does not match cited source line")
    return {"records_verified": len(records)}


TEST_RUNNER = clean('''
    import contextlib, io, json, sys, unittest
    sys.dont_write_bytecode = True
    sys.path.insert(0, sys.argv[1])
    with contextlib.redirect_stdout(sys.stderr):
        suite = unittest.defaultTestLoader.discover(sys.argv[1] + "/generated", pattern="test_labels.py")
        result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    print(json.dumps({"count": result.testsRun, "failures": len(result.failures),
                      "errors": len(result.errors), "skipped": len(result.skipped),
                      "expected_failures": len(result.expectedFailures),
                      "unexpected_successes": len(result.unexpectedSuccesses)}))
''')


CONFIG_RUNNER = clean('''
    import contextlib, dataclasses, importlib.util, json, sys, typing
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("mirror_config", sys.argv[1])
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    with contextlib.redirect_stdout(sys.stderr):
        spec.loader.exec_module(module)
        cls = module.MirrorConfig
        expected_types = {"mirror_id": str, "endpoint": str, "transport": typing.Literal["http", "https"],
                          "enabled": bool, "retry_limit": int}
        assert module.Transport == expected_types["transport"]
        assert dataclasses.is_dataclass(cls)
        fields = dataclasses.fields(cls)
        assert [f.name for f in fields] == list(expected_types)
        assert typing.get_type_hints(cls) == expected_types
        assert all(not f.kw_only and f.init and f.repr and f.compare for f in fields)
        assert all(f.default is dataclasses.MISSING for f in fields[:2])
        assert all(f.default_factory is dataclasses.MISSING for f in fields)
        assert [f.default for f in fields[2:]] == ["https", True, 3]
        assert type(fields[3].default) is bool and type(fields[4].default) is int
        value = cls("sample", "https://example.test")
        assert vars(value) == {"mirror_id": "sample", "endpoint": "https://example.test",
                               "transport": "https", "enabled": True, "retry_limit": 3}
        assert value == cls("sample", "https://example.test")
        assert "mirror_id='sample'" in repr(value)
        try:
            value.enabled = False
        except dataclasses.FrozenInstanceError:
            pass
        else:
            raise AssertionError("MirrorConfig is mutable")
        with open(sys.argv[2], encoding="utf-8") as profile_file:
            profiles = json.load(profile_file)["profiles"]
        for profile in profiles:
            assert dataclasses.asdict(cls(**profile)) == profile
    print(json.dumps({"profiles_constructed": len(profiles), "fields_verified": len(fields)}))
''')


def run_python(program, *arguments):
    # Fixed Python invocations only; never interpret a submitted command or shell string.
    result = subprocess.run([sys.executable, "-I", "-B", "-c", program, *map(str, arguments)],
                            capture_output=True, text=True, timeout=15, check=False)
    if result.returncode != 0:
        raise ValueError("Python validation failed: " + result.stderr[-1200:].strip())
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise ValueError("Validation did not produce one valid result object") from error


def check_python(path, run_id, permitted_imports):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    declarations = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        else:
            continue
        for target in targets:
            for name in ast.walk(target):
                if isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store) and name.id == "FIXTURE_RUN":
                    declarations.append(None if isinstance(node, ast.AugAssign) else node.value)
    if (len(declarations) != 1 or not isinstance(declarations[0], ast.Constant)
            or declarations[0].value != run_id):
        raise ValueError("FIXTURE_RUN must be declared exactly once with the current literal run ID")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module]
            if node.level:
                raise ValueError("Relative imports are outside the fixture contract")
        else:
            continue
        if any(module not in permitted_imports for module in modules):
            raise ValueError("Imports outside the fixture contract")
    return tree


def grade_tests(worker, run_id):
    submitted = worker / "generated/test_labels.py"
    check_python(submitted, run_id, {"unittest", "app.labels"})
    with tempfile.TemporaryDirectory(prefix="bounded-pilot-grade-") as temp:
        scratch = Path(temp)
        write(scratch / "app/__init__.py", "")
        write(scratch / "generated/test_labels.py", submitted.read_text(encoding="utf-8"))
        write(scratch / "app/labels.py", LABELS)
        reference = run_python(TEST_RUNNER, scratch)
        if reference["count"] < 5 or any(value for key, value in reference.items() if key != "count"):
            raise ValueError("Suite must discover at least five tests and pass reference without skips or expected failures")
        killed = []
        survived = []
        for name, (old, new) in MUTATIONS.items():
            if LABELS.count(old) != 1:
                raise ValueError("Invalid internal mutant definition")
            write(scratch / "app/labels.py", LABELS.replace(old, new))
            result = run_python(TEST_RUNNER, scratch)
            valid_run = (result["count"] == reference["count"] and not result["skipped"]
                         and not result["expected_failures"] and not result["unexpected_successes"])
            if valid_run and result["failures"] + result["errors"] > 0:
                killed.append(name)
            else:
                survived.append(name)
        return {"passed": not survived, "tests_discovered": reference["count"],
                "mutants_killed": killed, "mutants_survived": survived}


def grade_config(worker, run_id):
    module = worker / "generated/mirror_config.py"
    tree = check_python(module, run_id, {"dataclasses", "typing", "__future__"})
    if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree)):
        raise ValueError("Custom methods/helpers are outside the scaffold contract")
    profile_path = worker / "generated/profiles.json"
    profiles = load_json(profile_path)
    expected = {"run_id": run_id, "profiles": [
        {"mirror_id": "primary", "endpoint": "https://primary.example.test/assets",
         "transport": "https", "enabled": True, "retry_limit": 3},
        {"mirror_id": "staging", "endpoint": "https://staging.example.test/assets",
         "transport": "https", "enabled": False, "retry_limit": 1},
        {"mirror_id": "loopback", "endpoint": "http://127.0.0.1:8080/assets",
         "transport": "http", "enabled": True, "retry_limit": 0},
    ]}
    if json.dumps(profiles, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise ValueError("Profiles have incorrect schema, values, types, order, or run_id")
    with tempfile.TemporaryDirectory(prefix="bounded-pilot-config-") as temp:
        scratch = Path(temp)
        write(scratch / "mirror_config.py", module.read_text(encoding="utf-8"))
        write(scratch / "profiles.json", profile_path.read_text(encoding="utf-8"))
        return run_python(CONFIG_RUNNER, scratch / "mirror_config.py", scratch / "profiles.json")


def check_plain_path(path: Path) -> stat_result:
    """Reject links without following them, including Windows directory junctions."""
    info = path.lstat()
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & reparse_flag:
        raise ValueError(f"Linked path outside fixture contract: {path}")
    return info


def check_plain_directory(path: Path) -> None:
    if not stat.S_ISDIR(check_plain_path(path).st_mode):
        raise ValueError(f"Expected fixture directory: {path}")


def fixture_entries(directory: Path) -> Iterator[tuple[Path, stat_result]]:
    """Check each directory before descending instead of traversing reparse points."""
    pending = [directory]
    while pending:
        for path in pending.pop().iterdir():
            info = check_plain_path(path)
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
            yield path, info


def grade(root):
    check_plain_directory(root)
    check_plain_path(root / "manifest.json")
    manifest = load_json(root / "manifest.json")
    if (not isinstance(manifest, dict) or manifest.get("format") != 1
            or not isinstance(manifest.get("run_id"), str)
            or len(manifest["run_id"]) != 32):
        raise ValueError("Invalid fixture manifest")
    run_id = manifest["run_id"]
    results = []
    for case in CASES:
        files, oracle = inputs(case, run_id)
        for arm in ARMS:
            worker = root / case / arm
            result = {"case": case, "arm": arm, "passed": False}
            try:
                check_plain_directory(root / case)
                check_plain_directory(worker)
                peer = root / case / next(other for other in ARMS if other != arm)
                try:
                    check_plain_directory(peer)
                except (OSError, ValueError):
                    pass  # An absent or invalid peer gets its own failed-arm result.
                else:
                    if worker.samefile(peer):
                        raise ValueError("Baseline and candidate must be distinct fixture directories")
                ignored_bytecode = []
                for path, info in fixture_entries(worker):
                    relative = path.relative_to(worker)
                    if stat.S_ISDIR(info.st_mode):
                        continue
                    if not stat.S_ISREG(info.st_mode):
                        raise ValueError(f"Non-file path outside fixture contract: {relative.as_posix()}")
                    if relative.as_posix() in files.keys() | OUTPUTS[case]:
                        continue
                    if "__pycache__" in relative.parts and path.suffix == ".pyc":
                        ignored_bytecode.append(relative.as_posix())
                    else:
                        raise ValueError(f"Unexpected output file: {relative.as_posix()}")
                if ignored_bytecode:
                    result["ignored_bytecode_files"] = sorted(ignored_bytecode)
                for name, original in files.items():
                    path = worker / name
                    check_plain_path(path)
                    if path.read_bytes() != original.encode("utf-8"):
                        raise ValueError(f"Supplied input changed: {name}")
                if case in ("p1", "p2"):
                    details = grade_read(worker, run_id, "records" if case == "p1" else "calls", oracle)
                elif case == "p3":
                    details = grade_tests(worker, run_id)
                else:
                    details = grade_config(worker, run_id)
                result.update({"passed": True, **details})
            except (OSError, ValueError, SyntaxError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
                result["error"] = f"{type(error).__name__}: {error}"
            results.append(result)
    return {"run_id": run_id, "passed": all(item["passed"] for item in results), "results": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("prepare", help="Create a fresh pair for each pilot").add_argument("--dest", type=Path, required=True)
    commands.add_parser("grader", aliases=["grade"], help="Grade all eight worker directories").add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.dest) if args.command == "prepare" else grade(args.root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"passed": False, "error": f"{type(error).__name__}: {error}"}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
