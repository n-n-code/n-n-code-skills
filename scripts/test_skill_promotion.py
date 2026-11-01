#!/usr/bin/env python3
"""Behavioral tests for local publication/recovery, using only isolated files."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / ".agents/skills/agentic-sdlc-improvement/scripts/promotion.py"
SPEC = importlib.util.spec_from_file_location("skill_promotion", HELPER)
promotion = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = promotion
SPEC.loader.exec_module(promotion)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))


def write_json(path, value):
    write(path, json.dumps(value))


class SimulatedCrash(BaseException):
    pass


CHILD_IMPORT = """
import importlib.util, sys
spec = importlib.util.spec_from_file_location('child_promotion', sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
policy = module.load_policy(sys.argv[2])
"""


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-promotion-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.repository = self.root / "repository"
        (self.repository / ".git").mkdir(parents=True)
        self.allowed = self.repository / ".agents/skills"
        self.allowed.mkdir(parents=True)
        self.installed = self.root / "installed"
        self.installed.mkdir()
        self.target = self.allowed / "example"
        self.candidate = self.root / "candidates/example"
        write(self.target / "SKILL.md", "baseline\n")
        write(self.target / "references/keep.txt", "keep\n")
        write(self.target / "obsolete.txt", b"old\x00bytes")
        write(self.candidate / "SKILL.md", "candidate\n")
        write(self.candidate / "references/keep.txt", "keep\n")
        write(self.candidate / "references/new.txt", b"new\x00bytes")
        (self.candidate / "empty").mkdir()
        self.evidence = self.root / "evaluation.json"
        write(self.evidence, '{"decision":"fixture, not real evaluation"}\n')
        self.guard = self.root / "protected-policy.txt"
        write(self.guard, "fixed evaluation conditions\n")
        self.metadata = self.repository / "README.md"
        write(self.metadata, "existing documentation\n")
        self.policy_path = self.root / "policy.json"
        self.policy_data = {"version": 1, "state_root": str(self.root / "transactions"),
                            "allowed_target_roots": [str(self.allowed), str(self.installed)],
                            "allowed_target_files": [str(self.metadata)],
                            "protected_paths": [str(self.guard)],
                            "helper_sha256": hashlib.sha256(HELPER.read_bytes()).hexdigest()}
        self.save_policy()

    def save_policy(self):
        write_json(self.policy_path, self.policy_data)
        self.policy = promotion.load_policy(self.policy_path)

    def request(self, targets=None, **updates):
        value = {"version": 1, "eligibility": {"class": "behavior", "evidence": str(self.evidence)},
                 "targets": targets or [{"path": str(self.target), "candidate": str(self.candidate), "kind": "directory"}]}
        value.update(updates)
        path = self.root / f"request-{uuid.uuid4().hex}.json"
        write_json(path, value)
        return path

    def prepare(self, targets=None):
        return promotion.prepare(self.policy, self.request(targets))["transaction"]

    def read_record(self, transaction):
        return json.loads((self.policy.state / transaction / "journal.json").read_text())

    def cli(self, *arguments):
        return subprocess.run([sys.executable, "-I", "-B", str(HELPER), *arguments,
                               "--policy", str(self.policy_path)], capture_output=True, text=True, timeout=20)

    def test_complete_package_apply_and_recover_preserve_bytes(self):
        before = promotion._manifest(self.target)
        expected = promotion._manifest(self.candidate)
        transaction = self.prepare()
        self.assertEqual(promotion._manifest(self.target), before)
        self.assertEqual(promotion.apply(self.policy, transaction)["status"], "applied")
        self.assertEqual(promotion._manifest(self.target), expected)
        self.assertFalse((self.target / "obsolete.txt").exists())
        self.assertEqual((self.target / "references/new.txt").read_bytes(), b"new\x00bytes")
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
        self.assertEqual(promotion._manifest(self.target), before)
        self.assertEqual(list(self.root.glob(".skill-promotion-*")), [])
        self.assertTrue((self.policy.state / "promotion.lock").is_file())

    def test_absent_install_and_exact_metadata_file_in_one_transaction(self):
        destination = self.installed / "example"
        metadata_candidate = self.root / "candidates/README.md"
        write(metadata_candidate, "new documentation\n")
        targets = [{"path": str(self.target), "candidate": str(self.candidate)},
                   {"path": str(destination), "candidate": str(self.candidate)},
                   {"path": str(self.metadata), "candidate": str(metadata_candidate), "kind": "file"}]
        transaction = self.prepare(targets)
        promotion.apply(self.policy, transaction)
        self.assertEqual(promotion._manifest(destination), promotion._manifest(self.candidate))
        self.assertEqual(self.metadata.read_text(), "new documentation\n")
        promotion.recover(self.policy, transaction)
        self.assertFalse(destination.exists())
        self.assertEqual(self.metadata.read_text(), "existing documentation\n")

    def test_file_addition_and_explicit_absence_deletion(self):
        for initial in (False, True):
            with self.subTest(initial=initial):
                if self.metadata.exists():
                    self.metadata.unlink()
                if initial:
                    write(self.metadata, b"remove this\0")
                    candidate = None
                else:
                    candidate = self.root / "candidate-file.txt"
                    write(candidate, b"create this\0")
                before = promotion._manifest(self.metadata)
                transaction = self.prepare([{"path": str(self.metadata), "candidate": str(candidate) if candidate else None, "kind": "file"}])
                promotion.apply(self.policy, transaction)
                self.assertEqual(self.metadata.exists(), not initial)
                promotion.recover(self.policy, transaction)
                self.assertEqual(promotion._manifest(self.metadata), before)

    def test_file_directory_transitions_are_recoverable(self):
        write(self.target / "file-to-directory", "original file")
        write(self.target / "directory-to-file/nested", "original child")
        write(self.candidate / "file-to-directory/child", "new child")
        write(self.candidate / "directory-to-file", "new file")
        before = promotion._manifest(self.target)
        transaction = self.prepare()
        promotion.apply(self.policy, transaction)
        self.assertEqual(promotion._manifest(self.target), promotion._manifest(self.candidate))
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
        self.assertEqual(promotion._manifest(self.target), before)

    def test_every_write_boundary_recovers_exact_baseline(self):
        before = promotion._manifest(self.target)
        initial = self.prepare()
        count = len(promotion._plan(self.read_record(initial)))
        for event in ("before_write", "after_write"):
            for stop in range(count):
                with self.subTest(event=event, operation=stop):
                    transaction = self.prepare()
                    def crash(current_event, index, record):
                        if (current_event, index) == (event, stop):
                            raise SimulatedCrash()
                    with self.assertRaises(SimulatedCrash):
                        promotion.apply(self.policy, transaction, _fault=crash)
                    self.assertEqual(self.read_record(transaction)["status"], "applying")
                    self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
                    self.assertEqual(promotion._manifest(self.target), before)

    def test_recovery_itself_can_resume_after_a_write(self):
        before = promotion._manifest(self.target)
        transaction = self.prepare()
        promotion.apply(self.policy, transaction)
        def crash(event, index, record):
            if event == "after_restore":
                raise SimulatedCrash()
        with self.assertRaises(SimulatedCrash):
            promotion.recover(self.policy, transaction, _fault=crash)
        self.assertEqual(self.read_record(transaction)["status"], "recovering")
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
        self.assertEqual(promotion._manifest(self.target), before)

    def test_external_edit_survives_conflicted_recovery_and_blocks_apply(self):
        first = self.prepare()
        second = self.prepare()
        promotion.apply(self.policy, first)
        write(self.target / "SKILL.md", "external edit must survive\n")
        result = promotion.recover(self.policy, first)
        self.assertEqual(result["status"], "conflicted")
        self.assertEqual((self.target / "SKILL.md").read_text(), "external edit must survive\n")
        self.assertEqual((self.target / "obsolete.txt").read_bytes(), b"old\x00bytes")
        with self.assertRaisesRegex(promotion.PromotionError, "unresolved"):
            promotion.apply(self.policy, second)
        write(self.target / "SKILL.md", "baseline\n")
        self.assertEqual(promotion.recover(self.policy, first)["status"], "recovered")

    def test_unexpected_added_file_is_preserved_and_not_called_recovered(self):
        transaction = self.prepare()
        promotion.apply(self.policy, transaction)
        write(self.target / "user-added.txt", "unrelated")
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "conflicted")
        self.assertEqual((self.target / "user-added.txt").read_text(), "unrelated")

    def test_stale_content_and_new_membership_fail_before_managed_writes(self):
        for change in ("SKILL.md", "new-unrelated.txt"):
            with self.subTest(change=change):
                transaction = self.prepare()
                original = (self.target / change).read_bytes() if (self.target / change).exists() else None
                write(self.target / change, "concurrent change")
                expected = promotion._manifest(self.target)
                with self.assertRaisesRegex(promotion.PromotionError, "Baseline changed"):
                    promotion.apply(self.policy, transaction)
                self.assertEqual(promotion._manifest(self.target), expected)
                if original is None:
                    (self.target / change).unlink()
                else:
                    write(self.target / change, original)

    def test_change_between_preflight_and_replace_is_preserved(self):
        transaction = self.prepare()
        def interfere(event, index, record):
            operation = record["operations"][index]
            if event == "before_write" and operation["path"] == "SKILL.md":
                write(self.target / "SKILL.md", "another editor")
        with self.assertRaisesRegex(promotion.PromotionError, "Concurrent target change"):
            promotion.apply(self.policy, transaction, _fault=interfere)
        self.assertEqual((self.target / "SKILL.md").read_text(), "another editor")
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "conflicted")

    def test_frozen_evidence_and_snapshots_cannot_be_replaced(self):
        for relative in ("evidence", "candidate/0/SKILL.md", "baseline/0/SKILL.md"):
            with self.subTest(relative=relative):
                transaction = self.prepare()
                write(self.policy.state / transaction / relative, "tampered")
                with self.assertRaisesRegex(promotion.PromotionError, "changed"):
                    promotion.apply(self.policy, transaction)
                self.assertEqual((self.target / "SKILL.md").read_text(), "baseline\n")

    def test_evidence_reference_is_frozen_not_reinterpreted(self):
        transaction = self.prepare()
        original = self.evidence.read_bytes()
        write(self.evidence, "a different later assessment")
        self.assertEqual((self.policy.state / transaction / "evidence").read_bytes(), original)
        self.assertEqual(promotion.apply(self.policy, transaction)["status"], "applied")

    def test_protected_guard_changes_and_candidate_changes_are_rejected(self):
        guarded = self.target / "scripts/guard.py"
        write(guarded, "immutable helper")
        write(self.candidate / "scripts/guard.py", "immutable helper")
        self.policy_data["protected_paths"].append(str(guarded))
        self.save_policy()
        transaction = self.prepare()
        write(self.guard, "edited policy")
        with self.assertRaisesRegex(promotion.PromotionError, "Protected"):
            promotion.apply(self.policy, transaction)
        write(self.guard, "fixed evaluation conditions\n")
        write(self.candidate / "scripts/guard.py", "changed helper")
        with self.assertRaisesRegex(promotion.PromotionError, "protected"):
            self.prepare()

    def test_policy_fingerprint_and_helper_pin_are_checked(self):
        transaction = self.prepare()
        self.policy_path.write_text(self.policy_path.read_text() + "\n")
        new_policy = promotion.load_policy(self.policy_path)
        with self.assertRaisesRegex(promotion.PromotionError, "Protected"):
            promotion.apply(new_policy, transaction)
        with mock.patch.object(promotion, "_target_path", side_effect=AssertionError("changed-policy target inspected")):
            self.assertTrue(promotion.status(new_policy, transaction)["inspection_requires_recorded_policy"])
        self.policy_data["helper_sha256"] = "0" * 64
        with self.assertRaisesRegex(promotion.PromotionError, "helper fingerprint"):
            self.save_policy()

    def foreign_transaction(self):
        target = self.root / "foreign-runtime.json"
        candidate = self.root / "foreign-candidate.json"
        write(target, "old runtime")
        write(candidate, "new runtime")
        data = dict(self.policy_data, allowed_target_roots=[], allowed_target_files=[str(target)])
        policy_path = self.root / "foreign-policy.json"
        write_json(policy_path, data)
        policy = promotion.load_policy(policy_path)
        request = self.request([{"path": str(target), "candidate": str(candidate), "kind": "file"}])
        transaction = promotion.prepare(policy, request)["transaction"]
        return policy, transaction, target

    def test_applied_foreign_policy_is_summarized_and_does_not_block_prepare(self):
        foreign, transaction, _ = self.foreign_transaction()
        promotion.apply(foreign, transaction)
        result = promotion.status(self.policy)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["status"], "applied")
        self.assertEqual(result[0]["policy"], str(foreign.path))
        self.assertTrue(result[0]["inspection_requires_recorded_policy"])
        self.assertNotIn("targets", result[0])
        self.prepare()

    def test_unresolved_foreign_policy_still_blocks_shared_publication(self):
        normal = self.prepare()
        foreign, transaction, _ = self.foreign_transaction()
        def crash(event, index, record):
            if event == "after_write":
                raise SimulatedCrash()
        with self.assertRaises(SimulatedCrash):
            promotion.apply(foreign, transaction, _fault=crash)
        with self.assertRaisesRegex(promotion.PromotionError, "unresolved"):
            promotion.apply(self.policy, normal)
        with self.assertRaisesRegex(promotion.PromotionError, "unresolved"):
            self.prepare()
        self.assertEqual(promotion.recover(foreign, transaction)["status"], "recovered")

    def test_explicit_foreign_status_never_inspects_targets_or_protected_paths(self):
        foreign, transaction, target = self.foreign_transaction()
        promotion.apply(foreign, transaction)
        with mock.patch.object(promotion, "_target_path", side_effect=AssertionError("foreign target inspected")), \
                mock.patch.object(promotion, "_fingerprints", side_effect=AssertionError("foreign guards inspected")):
            result = promotion.status(self.policy, transaction)
        self.assertTrue(result["inspection_requires_recorded_policy"])
        self.assertEqual(target.read_text(), "new runtime")
        with self.assertRaisesRegex(promotion.PromotionError, "policy differs"):
            promotion.recover(self.policy, transaction)

    def test_unknown_schema_and_incorrect_kinds_fail_closed(self):
        request = self.request(unexpected=True)
        with self.assertRaises(promotion.PromotionError):
            promotion.prepare(self.policy, request)
        with self.assertRaises(promotion.PromotionError):
            self.prepare([{"path": str(self.metadata), "candidate": str(self.candidate), "kind": "directory"}])
        self.policy_data["disable_protections"] = True
        with self.assertRaises(promotion.PromotionError):
            self.save_policy()

    def test_unsafe_scope_and_overlaps_are_rejected(self):
        cases = [
            [{"path": str(self.allowed), "candidate": str(self.candidate)}],
            [{"path": str(self.root / "outside"), "candidate": str(self.candidate)}],
            [{"path": "relative", "candidate": str(self.candidate)}],
            [{"path": str(self.allowed / ".." / "escape"), "candidate": str(self.candidate)}],
            [{"path": str(self.target), "candidate": str(self.target)}],
            [{"path": str(self.target), "candidate": str(self.candidate)},
             {"path": str(self.target / "references"), "candidate": str(self.candidate)}],
        ]
        for targets in cases:
            with self.subTest(targets=targets), self.assertRaises(promotion.PromotionError):
                self.prepare(targets)

    def test_state_and_candidates_must_be_outside_checkouts(self):
        with self.assertRaisesRegex(promotion.PromotionError, "outside checkouts"):
            self.prepare([{"path": str(self.installed / "new"), "candidate": str(self.target)}])
        self.policy_data["state_root"] = str(self.repository / "state")
        with self.assertRaisesRegex(promotion.PromotionError, "outside Git"):
            self.save_policy()

    def test_unreadable_directory_is_not_an_empty_manifest(self):
        with mock.patch.object(promotion.os, "scandir", side_effect=PermissionError("fixture denied enumeration")):
            with self.assertRaisesRegex(promotion.PromotionError, "Cannot enumerate complete tree"):
                promotion._manifest(self.target)

    def test_cancel_unapplied_transaction_preserves_later_external_changes(self):
        transaction = self.prepare()
        write(self.target / "SKILL.md", "later user work")
        result = promotion.recover(self.policy, transaction)
        self.assertEqual(result["status"], "cancelled")
        self.assertEqual((self.target / "SKILL.md").read_text(), "later user work")
        self.prepare()  # A cancellation is terminal and does not block another experiment.

    def test_version_boolean_and_case_varied_git_metadata_are_rejected(self):
        with self.assertRaisesRegex(promotion.PromotionError, "version"):
            promotion.prepare(self.policy, self.request(version=True))
        with self.assertRaises(promotion.PromotionError):
            self.prepare([{"path": str(self.allowed / ".GIT"), "candidate": str(self.candidate)}])
        write(self.candidate / ".GIT/config", "not package content")
        with self.assertRaises(promotion.PromotionError):
            self.prepare()

    def test_repeated_recovery_reports_later_drift_without_modifying_it(self):
        transaction = self.prepare()
        promotion.apply(self.policy, transaction)
        promotion.recover(self.policy, transaction)
        write(self.target / "SKILL.md", "legitimate work after rollback")
        result = promotion.recover(self.policy, transaction)
        self.assertEqual(result["status"], "recovered")
        self.assertTrue(result["already_recovered"])
        self.assertFalse(result["targets"][0]["matches_baseline"])
        self.assertEqual((self.target / "SKILL.md").read_text(), "legitimate work after rollback")

    def test_unchanged_readonly_file_survives_snapshot_and_stage_cleanup(self):
        import stat
        source = self.target / "immutable.txt"
        candidate = self.candidate / "immutable.txt"
        write(source, "same")
        write(candidate, "same")
        source.chmod(stat.S_IREAD)
        candidate.chmod(stat.S_IREAD)
        transaction = self.prepare()
        self.assertEqual(promotion.apply(self.policy, transaction)["status"], "applied")
        self.assertEqual(source.read_text(), "same")
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")

    @unittest.skipUnless(os.name == "nt", "Windows read-only replacement boundary")
    def test_windows_readonly_changes_are_rejected_during_prepare(self):
        import stat
        cases = [(self.candidate / "SKILL.md", "writable to read-only"),
                 (self.target / "SKILL.md", "read-only to writable"),
                 (self.target / "obsolete.txt", "read-only removal"),
                 (self.candidate / "references/new.txt", "new read-only file")]
        for path, label in cases:
            with self.subTest(case=label):
                mode = path.stat().st_mode
                path.chmod(stat.S_IREAD)
                before = promotion._manifest(self.target)
                try:
                    with self.assertRaisesRegex(promotion.PromotionError, "Windows read-only"):
                        self.prepare()
                    self.assertEqual(promotion._manifest(self.target), before)
                finally:
                    path.chmod(mode)

    @unittest.skipUnless(os.name == "nt", "Windows read-only replacement boundary")
    def test_windows_apply_rechecks_readonly_plan_before_managed_writes(self):
        import stat
        (self.candidate / "SKILL.md").chmod(stat.S_IREAD)
        before = promotion._manifest(self.target)
        # Model a previously prepared record; apply must enforce its own boundary.
        with mock.patch.object(promotion, "_validate_operations"):
            transaction = self.prepare()
        with self.assertRaisesRegex(promotion.PromotionError, "Windows read-only"):
            promotion.apply(self.policy, transaction)
        self.assertEqual(promotion._manifest(self.target), before)
        self.assertEqual(self.read_record(transaction)["status"], "prepared")

    @unittest.skipUnless(os.name == "nt", "Windows DACL inheritance boundary")
    def test_windows_new_files_inherit_destination_access_not_private_stage(self):
        readable_parent = "D:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;FA;;;OW)(A;OICI;0x1200a9;;;BU)"
        promotion._set_dacl(self.installed, readable_parent)
        destination = self.installed / "example"
        transaction = self.prepare([{"path": str(destination), "candidate": str(self.candidate)}])
        snapshot = self.policy.state / transaction / "candidate/0/SKILL.md"
        self.assertNotIn(";;;BU)", promotion._dacl(snapshot))
        promotion.apply(self.policy, transaction)
        reference = destination / "ordinary-created-file.txt"
        write(reference, "independent default creation")
        actual = promotion._dacl(destination / "SKILL.md")
        self.assertEqual(actual, promotion._dacl(reference))
        self.assertIn(";;;BU)", actual)
        self.assertFalse(actual.split("(")[0].startswith("D:P"))
        reference.unlink()
        self.assertNotIn(";;;BU)", promotion._dacl(snapshot))
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
        self.assertFalse(destination.exists())

    @unittest.skipUnless(os.name == "nt", "Windows private publication boundary")
    def test_windows_private_target_permissions_exist_before_copying_bytes(self):
        readable_parent = "D:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;FA;;;OW)(A;OICI;0x1200a9;;;BU)"
        private = "D:P(A;;FA;;;SY)(A;;FA;;;BA)(A;;FA;;;OW)"
        promotion._set_dacl(self.installed, readable_parent)
        source = self.target / "SKILL.md"
        publication = self.installed / "private-publication.tmp"
        copied = []
        original_copy = shutil.copyfileobj
        def observe_before_copy(input_stream, output, *args):
            copied.append(promotion._dacl(publication))
            self.assertEqual(copied[-1], private)
            return original_copy(input_stream, output, *args)
        with mock.patch.object(shutil, "copyfileobj", side_effect=observe_before_copy):
            promotion._native_publication_file(source, publication, private)
        self.assertEqual(copied, [private])
        self.assertEqual(publication.read_bytes(), source.read_bytes())
        self.assertEqual(promotion._dacl(publication), private)

    @unittest.skipUnless(os.name == "nt", "Windows DACL restoration boundary")
    def test_windows_custom_dacls_survive_replacement_deletion_and_restore(self):
        custom_file = "D:P(A;;FA;;;SY)(A;;FA;;;BA)(A;;FA;;;OW)(A;;0x1200a9;;;BU)"
        custom_dir = "D:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;FA;;;OW)(A;OICI;0x1200a9;;;BU)"
        promotion._set_dacl(self.target / "SKILL.md", custom_file)
        promotion._set_dacl(self.target / "obsolete.txt", custom_file)
        removed_dir = self.target / "removed-directory"
        removed_dir.mkdir()
        promotion._set_dacl(removed_dir, custom_dir)
        write(removed_dir / "child.txt", "restored child")
        write(self.target / "file-to-directory", "original file")
        promotion._set_dacl(self.target / "file-to-directory", custom_file)
        write(self.candidate / "file-to-directory/child", "new nested file")
        replaced_dir = self.target / "directory-to-file"
        replaced_dir.mkdir()
        promotion._set_dacl(replaced_dir, custom_dir)
        write(replaced_dir / "child", "old child")
        write(self.candidate / "directory-to-file", "new file")
        before = promotion._permissions(self.target)
        transaction = self.prepare()
        promotion.apply(self.policy, transaction)
        self.assertEqual(promotion._dacl(self.target / "SKILL.md"), before["SKILL.md"])
        self.assertFalse(removed_dir.exists())
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
        self.assertEqual(promotion._permissions(self.target), before)

    @unittest.skipUnless(os.name == "nt", "Windows permission-only conflict")
    def test_windows_permission_only_edit_is_preserved_as_a_conflict(self):
        custom = "D:P(A;;FA;;;SY)(A;;FA;;;BA)(A;;FA;;;OW)(A;;0x1200a9;;;BU)"
        transaction = self.prepare()
        promotion.apply(self.policy, transaction)
        path = self.target / "SKILL.md"
        promotion._set_dacl(path, custom)
        changed = promotion._dacl(path)
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "conflicted")
        self.assertEqual(path.read_text(), "candidate\n")
        self.assertEqual(promotion._dacl(path), changed)

    @unittest.skipUnless(os.name == "nt", "Windows DACL preflight")
    def test_windows_parent_and_existing_dacl_drift_fail_preflight(self):
        custom = "D:P(A;;FA;;;SY)(A;;FA;;;BA)(A;;FA;;;OW)(A;;0x1200a9;;;BU)"
        transaction = self.prepare()
        path = self.target / "SKILL.md"
        promotion._set_dacl(path, custom)
        with self.assertRaisesRegex(promotion.PromotionError, "Baseline changed"):
            promotion.apply(self.policy, transaction)
        self.assertEqual(path.read_text(), "baseline\n")
        destination = self.installed / "absent"
        transaction = self.prepare([{"path": str(destination), "candidate": str(self.candidate)}])
        promotion._set_dacl(self.installed, "D:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;FA;;;OW)(A;OICI;0x1200a9;;;BU)")
        with self.assertRaisesRegex(promotion.PromotionError, "Baseline changed"):
            promotion.apply(self.policy, transaction)
        self.assertFalse(destination.exists())

    @unittest.skipUnless(os.name == "nt", "Windows publication staging failure")
    def test_windows_dacl_failure_does_not_replace_active_file(self):
        candidate = self.root / "new-readme.txt"
        write(candidate, "candidate metadata")
        original = self.metadata.read_bytes()
        original_dacl = promotion._dacl(self.metadata)
        transaction = self.prepare([{"path": str(self.metadata), "candidate": str(candidate), "kind": "file"}])
        with mock.patch.object(promotion, "_set_dacl", side_effect=OSError("fixture ACL failure")):
            with self.assertRaisesRegex(promotion.PromotionError, "ACL failure"):
                promotion.apply(self.policy, transaction)
        self.assertEqual(self.metadata.read_bytes(), original)
        self.assertEqual(promotion._dacl(self.metadata), original_dacl)
        self.assertEqual(list(self.repository.glob(".skill-publish-*")), [])
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")

    @unittest.skipUnless(os.name == "nt", "Windows publication temporary recovery")
    def test_process_death_after_publication_stage_cleans_owned_temporary(self):
        before = promotion._manifest(self.target)
        permissions = promotion._permissions(self.target)
        transaction = self.prepare()
        code = CHILD_IMPORT + """
import os
def die(event, index, record):
    if event == 'after_publication_stage':
        os._exit(77)
module.apply(policy, sys.argv[3], _fault=die)
"""
        child = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(HELPER), str(self.policy_path), transaction],
                               capture_output=True, text=True, timeout=15)
        self.assertEqual(child.returncode, 77, child.stderr)
        self.assertTrue(list(self.target.rglob(".skill-publish-*")))
        self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
        self.assertEqual(list(self.target.rglob(".skill-publish-*")), [])
        self.assertEqual(promotion._manifest(self.target), before)
        self.assertEqual(promotion._permissions(self.target), permissions)

    def test_symlink_or_junction_cannot_redirect_a_target(self):
        real = self.root / "external"
        real.mkdir()
        write(real / "keep", "untouched")
        link = self.allowed / "linked"
        if os.name == "nt":
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(real)],
                                    capture_output=True, text=True, timeout=10)
            if result.returncode:
                self.skipTest("Windows junction creation unavailable")
            self.addCleanup(lambda: os.rmdir(link) if link.exists() else None)
        else:
            link.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(promotion.PromotionError, "reparse|Links"):
            self.prepare([{"path": str(link), "candidate": str(self.candidate)}])
        self.assertEqual((real / "keep").read_text(), "untouched")

    def test_operation_journal_cannot_add_a_write(self):
        transaction = self.prepare()
        record = self.read_record(transaction)
        record["operations"] = [{"target": 0, "path": "../../escape", "before": None, "after": None, "state": "done"}]
        write_json(self.policy.state / transaction / "journal.json", record)
        with self.assertRaisesRegex(promotion.PromotionError, "journal"):
            promotion.recover(self.policy, transaction)

    def test_cli_prepare_status_apply_recover(self):
        request = self.request()
        prepared = self.cli("prepare", "--request", str(request))
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        transaction = json.loads(prepared.stdout)["transaction"]
        inspected = self.cli("status", "--transaction", transaction)
        self.assertTrue(json.loads(inspected.stdout)["targets"][0]["matches_baseline"])
        applied = self.cli("apply", "--transaction", transaction)
        self.assertEqual(applied.returncode, 0, applied.stderr)
        recovered = self.cli("recover", "--transaction", transaction)
        self.assertEqual(recovered.returncode, 0, recovered.stderr)

    def test_real_concurrent_publishers_are_serialized(self):
        first, second = self.prepare(), self.prepare()
        code = CHILD_IMPORT + """
def pause(event, index, record):
    if event == 'before_write' and index == 0:
        print('locked', flush=True)
        sys.stdin.readline()
module.apply(policy, sys.argv[3], _fault=pause)
"""
        child = subprocess.Popen([sys.executable, "-I", "-B", "-c", code, str(HELPER), str(self.policy_path), first],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(), "locked")
            blocked = self.cli("apply", "--transaction", second)
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("global lock", blocked.stderr)
            output, error = child.communicate("continue\n", timeout=15)
            self.assertEqual(child.returncode, 0, error)
            stale = self.cli("apply", "--transaction", second)
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("Baseline changed", stale.stderr)
        finally:
            if child.poll() is None:
                child.kill()
                child.communicate(timeout=5)

    def test_process_death_releases_lock_but_journal_blocks_new_apply(self):
        before = promotion._manifest(self.target)
        first, second = self.prepare(), self.prepare()
        code = CHILD_IMPORT + """
import os
def die(event, index, record):
    if event == 'after_write':
        os._exit(77)
module.apply(policy, sys.argv[3], _fault=die)
"""
        child = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(HELPER), str(self.policy_path), first],
                               capture_output=True, text=True, timeout=15)
        self.assertEqual(child.returncode, 77, child.stderr)
        blocked = self.cli("apply", "--transaction", second)
        self.assertIn("unresolved", blocked.stderr)
        self.assertNotIn("global lock", blocked.stderr)
        self.assertEqual(promotion.recover(self.policy, first)["status"], "recovered")
        self.assertEqual(promotion._manifest(self.target), before)
        self.assertEqual(list(self.root.glob(".skill-promotion-*")), [])

    @unittest.skipUnless(os.name == "nt", "Windows cross-drive publication test")
    def test_state_on_c_and_managed_target_on_d(self):
        if self.root.drive.lower() == ROOT.drive.lower():
            self.skipTest("Test storage and source checkout use the same drive")
        with tempfile.TemporaryDirectory(prefix="skill-promotion-test-", dir=ROOT.parent) as other:
            allowed = Path(other)
            target = allowed / "package"
            self.policy_data["allowed_target_roots"].append(str(allowed))
            self.save_policy()
            transaction = self.prepare([{"path": str(target), "candidate": str(self.candidate)}])
            self.assertEqual(promotion.apply(self.policy, transaction)["status"], "applied")
            self.assertEqual(promotion._manifest(target), promotion._manifest(self.candidate))
            self.assertEqual(promotion.recover(self.policy, transaction)["status"], "recovered")
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
