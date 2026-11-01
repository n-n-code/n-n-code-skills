#!/usr/bin/env python3
"""Publish frozen local skill packages with conflict-aware recovery (Python 3.10+).

This utility checks filesystem preconditions, not the truth of evaluation evidence.
The lock coordinates users of this utility; publication is atomic per file, not per
package. Other editors/readers are not locked out. No Git, network, or grader runs.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
from typing import Callable
import uuid


class PromotionError(Exception):
    """An invalid request, stale precondition, or unresolved publication."""


UNRESOLVED = {"applying", "interrupted", "recovering", "conflicted"}
CLASSES = {"bootstrap", "maintenance", "behavior", "improver"}
TRANSACTION_ID = re.compile(r"[0-9a-f]{32}\Z")
JOURNAL_VERSION = 3
TERMINAL = {"prepared", "applied", "recovered", "cancelled"}
OPERATION_STATES = {"pending", "intent", "done", "undo_intent", "undone", "conflicted"}


@lru_cache(maxsize=1)
def _windows_api():
    import ctypes
    from ctypes import wintypes
    security = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    pointer = ctypes.c_void_p
    out_pointer = ctypes.POINTER(pointer)
    security.GetNamedSecurityInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                              out_pointer, out_pointer, out_pointer, out_pointer, out_pointer]
    security.GetNamedSecurityInfoW.restype = wintypes.DWORD
    security.ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes = [pointer, wintypes.DWORD, wintypes.DWORD, out_pointer, ctypes.POINTER(wintypes.DWORD)]
    security.ConvertSecurityDescriptorToStringSecurityDescriptorW.restype = wintypes.BOOL
    security.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, out_pointer, ctypes.POINTER(wintypes.DWORD)]
    security.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL
    security.GetSecurityDescriptorDacl.argtypes = [pointer, ctypes.POINTER(wintypes.BOOL), out_pointer, ctypes.POINTER(wintypes.BOOL)]
    security.GetSecurityDescriptorDacl.restype = wintypes.BOOL
    security.GetSecurityDescriptorControl.argtypes = [pointer, ctypes.POINTER(wintypes.WORD), ctypes.POINTER(wintypes.DWORD)]
    security.GetSecurityDescriptorControl.restype = wintypes.BOOL
    security.SetNamedSecurityInfoW.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, pointer, pointer, pointer, pointer]
    security.SetNamedSecurityInfoW.restype = wintypes.DWORD
    kernel.LocalFree.argtypes = [pointer]
    kernel.LocalFree.restype = pointer
    kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, pointer, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    return ctypes, wintypes, security, kernel


def _dacl(path: Path) -> str | None:
    if os.name != "nt" or not path.exists():
        return None
    _safe_path(path)
    ctypes, _, security, kernel = _windows_api()
    descriptor, rendered = ctypes.c_void_p(), ctypes.c_void_p()
    error = security.GetNamedSecurityInfoW(str(path), 1, 4, None, None, None, None, ctypes.byref(descriptor))
    if error:
        raise ctypes.WinError(error)
    try:
        if not security.ConvertSecurityDescriptorToStringSecurityDescriptorW(descriptor, 1, 4, ctypes.byref(rendered), None):
            raise ctypes.WinError(ctypes.get_last_error())
        value = ctypes.wstring_at(rendered.value)
        header, separator, aces = value.partition("(")
        # SetNamedSecurityInfo marks legacy ACLs auto-inherited (AI) without
        # changing their ACEs or protected/unprotected inheritance semantics.
        return header.replace("AI", "") + separator + aces
    finally:
        kernel.LocalFree(rendered)
        kernel.LocalFree(descriptor)


def _set_dacl(path: Path, value: str) -> None:
    """Copy a saved file/directory DACL, including its inheritance protection."""
    _safe_path(path)
    ctypes, wintypes, security, kernel = _windows_api()
    descriptor, acl = ctypes.c_void_p(), ctypes.c_void_p()
    present, defaulted = wintypes.BOOL(), wintypes.BOOL()
    control, revision = wintypes.WORD(), wintypes.DWORD()
    if not security.ConvertStringSecurityDescriptorToSecurityDescriptorW(value, 1, ctypes.byref(descriptor), None):
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        if not security.GetSecurityDescriptorDacl(descriptor, ctypes.byref(present), ctypes.byref(acl), ctypes.byref(defaulted)):
            raise ctypes.WinError(ctypes.get_last_error())
        if not security.GetSecurityDescriptorControl(descriptor, ctypes.byref(control), ctypes.byref(revision)):
            raise ctypes.WinError(ctypes.get_last_error())
        if not present.value:
            raise PromotionError("A saved DACL is required")
        flags = 4 | (0x80000000 if control.value & 0x1000 else 0x20000000)
        error = security.SetNamedSecurityInfoW(str(path), 1, flags, None, None, acl, None)
        if error:
            raise ctypes.WinError(error)
    finally:
        kernel.LocalFree(descriptor)
    if _dacl(path) != value:
        raise PromotionError(f"DACL restoration did not preserve expected permissions: {path}")


def _permissions(path: Path, manifest: dict | None = None) -> dict:
    if os.name != "nt":
        return {}
    manifest = _manifest(path) if manifest is None else manifest
    return {relative: _dacl(path / relative if relative else path) for relative in manifest}


def _native_publication_file(source: Path, destination: Path, saved_dacl: str | None = None) -> None:
    """Create in the actual destination parent, with native inherited security."""
    import msvcrt
    ctypes, wintypes, security, kernel = _windows_api()
    descriptor = ctypes.c_void_p()
    attributes = None
    if saved_dacl is not None:
        class SecurityAttributes(ctypes.Structure):
            _fields_ = [("length", wintypes.DWORD), ("descriptor", ctypes.c_void_p), ("inherit", wintypes.BOOL)]
        if not security.ConvertStringSecurityDescriptorToSecurityDescriptorW(saved_dacl, 1, ctypes.byref(descriptor), None):
            raise ctypes.WinError(ctypes.get_last_error())
        attributes = SecurityAttributes(ctypes.sizeof(SecurityAttributes), descriptor, False)
    try:
        handle = kernel.CreateFileW(str(destination), 0x40000000, 0,
                                    ctypes.byref(attributes) if attributes else None, 1, 0x80, None)
        error = ctypes.get_last_error()
    finally:
        kernel.LocalFree(descriptor)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(error)
    try:
        # A private existing target must never pass through broader inherited
        # access while its candidate bytes are written to this temporary file.
        if saved_dacl is not None and _dacl(destination) != saved_dacl:
            raise PromotionError("Native publication creation changed the saved DACL")
        descriptor = msvcrt.open_osfhandle(handle, os.O_WRONLY | os.O_BINARY)
    except BaseException:
        kernel.CloseHandle(handle)
        raise
    with os.fdopen(descriptor, "wb") as output, source.open("rb") as input_stream:
        shutil.copyfileobj(input_stream, output)
        output.flush()
        os.fsync(output.fileno())
    shutil.copystat(source, destination)


def _object(value, allowed, required):
    if not isinstance(value, dict) or set(value) - set(allowed) or set(required) - set(value):
        raise PromotionError("Missing or unknown JSON fields")
    return value


def _enum(value, choices, label: str):
    if not isinstance(value, str) or value not in choices:
        raise PromotionError(f"Invalid {label}")
    return value


def _mode(value) -> int:
    if type(value) is not int or not 0 <= value <= 0o7777:
        raise PromotionError("Invalid permission mode")
    return value


def _mode_guards(value) -> None:
    if not isinstance(value, dict):
        raise PromotionError("Invalid ancestor mode guards")
    for path, mode in value.items():
        _path(path)
        _mode(mode)


def _journal_header(record, transaction: str) -> None:
    if not isinstance(record, dict):
        raise PromotionError("Invalid transaction record")
    if type(record.get("version")) is not int or record["version"] < 1:
        raise PromotionError("Invalid journal version")
    if record.get("id") != transaction:
        raise PromotionError("Transaction identity differs")
    _enum(record.get("status"), UNRESOLVED | TERMINAL, "transaction status")
    _lexical_path(record.get("policy"))
    if not isinstance(record.get("policy_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["policy_sha256"]):
        raise PromotionError("Invalid policy fingerprint")


def _read_json(path: Path):
    _safe_path(path)
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError) as exc:
        raise PromotionError(f"Cannot read JSON: {path}: {exc}") from exc


def _safe_path(path: Path) -> None:
    """Reject links/reparse points in every existing component, without following them."""
    for part in (*reversed(path.parents), path):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise PromotionError(f"Links or reparse points are not supported: {part}")


def _lexical_path(value) -> Path:
    if not isinstance(value, str) or not value or "\0" in value:
        raise PromotionError("Paths must be nonempty absolute strings")
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise PromotionError(f"Absolute paths without traversal are required: {value}")
    path = Path(os.path.abspath(path))
    return path


def _path(value) -> Path:
    path = _lexical_path(value)
    _safe_path(path)
    return path


def _within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _overlap(first: Path, second: Path) -> bool:
    return _within(first, second) or _within(second, first)


def _checkout(path: Path) -> Path | None:
    for parent in (path, *path.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _entry(path: Path):
    _safe_path(path)
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISDIR(info.st_mode):
        return {"kind": "directory", **({"mode": stat.S_IMODE(info.st_mode)} if os.name != "nt" else {})}
    if stat.S_ISREG(info.st_mode):
        return {"kind": "file", "sha256": _digest(path), "mode": stat.S_IMODE(info.st_mode)}
    raise PromotionError(f"Only regular files and directories are supported: {path}")


def _manifest(path: Path) -> dict:
    root = _entry(path)
    if root is None:
        return {}
    result = {"": root}
    if root["kind"] == "directory":
        def enumeration_error(error):
            raise PromotionError(f"Cannot enumerate complete tree: {error}") from error
        for directory, names, files in os.walk(path, followlinks=False, onerror=enumeration_error):
            for name in sorted(names + files):
                child = Path(directory) / name
                relative = child.relative_to(path).as_posix()
                _relative(relative)
                result[relative] = _entry(child)
                if result[relative] is None:
                    raise PromotionError(f"Tree changed during inspection: {child}")
    return result


def _relative(value: str) -> None:
    if not isinstance(value, str) or (value and (
        value.startswith("/") or "\\" in value or ":" in value
        or any(part in {"", ".", ".."} or part.casefold() == ".git" for part in value.split("/"))
    )):
        raise PromotionError(f"Unsafe manifest path: {value!r}")


def _validate_manifest(value, *, posix: bool | None = None) -> None:
    posix = os.name != "nt" if posix is None else posix
    if not isinstance(value, dict):
        raise PromotionError("Invalid tree manifest")
    for relative, entry in value.items():
        _relative(relative)
        if not isinstance(entry, dict):
            raise PromotionError("Invalid manifest entry")
        _enum(entry.get("kind"), {"file", "directory"}, "manifest kind")
        if entry["kind"] == "directory":
            fields = {"kind", "mode"} if posix else {"kind"}
            _object(entry, fields, fields)
            if posix:
                _mode(entry["mode"])
        else:
            _object(entry, {"kind", "sha256", "mode"}, {"kind", "sha256", "mode"})
            if not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
                raise PromotionError("Invalid file fingerprint")
            _mode(entry["mode"])
    if value and "" not in value:
        raise PromotionError("Manifest is missing its root")


def _supported_directory_modes(manifest: dict) -> None:
    if os.name != "nt":
        for entry in manifest.values():
            if entry["kind"] == "directory" and (entry["mode"] & ~0o777 or entry["mode"] & 0o500 != 0o500):
                raise PromotionError("POSIX directories require owner read/execute and no special permission bits")


def _atomic_json(path: Path, value) -> None:
    _safe_path(path)
    descriptor, temporary = tempfile.mkstemp(prefix=".journal-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _copy_file(source: Path, destination: Path) -> None:
    # Windows fsync needs a writable descriptor; apply read-only metadata last.
    shutil.copyfile(source, destination)
    with destination.open("r+b") as stream:
        stream.flush()
        os.fsync(stream.fileno())
    shutil.copystat(source, destination)


def _copy_snapshot(source: Path, destination: Path, expected: dict) -> None:
    if _manifest(source) != expected:
        raise PromotionError(f"Snapshot source changed: {source}")
    for relative, entry in sorted(expected.items(), key=lambda item: (item[0].count("/"), item[0])):
        target = destination / relative if relative else destination
        if entry["kind"] == "directory":
            target.mkdir(mode=0o700, parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            _copy_file(source / relative if relative else source, target)
    if os.name != "nt":
        for relative, entry in sorted(expected.items(), key=lambda item: _depth(item[0]), reverse=True):
            if entry["kind"] == "directory":
                (destination / relative if relative else destination).chmod(entry["mode"])
    if _manifest(destination) != expected or _manifest(source) != expected:
        raise PromotionError(f"Snapshot verification failed: {source}")


@dataclass(frozen=True)
class Policy:
    path: Path
    state: Path
    roots: tuple[Path, ...]
    files: tuple[Path, ...]
    protected: tuple[Path, ...]
    fingerprint: str


def load_policy(path: str | Path) -> Policy:
    path = _path(str(path))
    raw = _read_json(path)
    fields = {"version", "state_root", "allowed_target_roots", "allowed_target_files", "protected_paths", "helper_sha256"}
    _object(raw, fields, fields)
    if type(raw["version"]) is not int or raw["version"] != 1:
        raise PromotionError("Unsupported policy version")
    for name in ("allowed_target_roots", "allowed_target_files", "protected_paths"):
        if not isinstance(raw[name], list):
            raise PromotionError(f"{name} must be a list")
    helper = _path(str(Path(__file__).absolute()))
    if raw["helper_sha256"] != _digest(helper):
        raise PromotionError("Running helper does not match the protected helper fingerprint")
    state = _path(raw["state_root"])
    if state.parent == state or _checkout(state):
        raise PromotionError("State must be outside Git checkouts and filesystem roots")
    roots = tuple(_path(value) for value in raw["allowed_target_roots"])
    files = tuple(_path(value) for value in raw["allowed_target_files"])
    if not roots and not files:
        raise PromotionError("Policy must allow at least one target")
    if any(not root.is_dir() for root in roots):
        raise PromotionError("Allowed target roots must be existing directories")
    protected = tuple(dict.fromkeys([path, helper, *(_path(value) for value in raw["protected_paths"])]))
    return Policy(path, state, roots, files, protected, _digest(path))


def _target_path(policy: Policy, value: str, kind: str) -> Path:
    path = _path(value)
    _enum(kind, {"directory", "file"}, "target kind")
    if any(part.casefold() == ".git" for part in path.parts):
        raise PromotionError("Invalid target kind or Git metadata target")
    allowed = any(path != root and _within(path, root) for root in policy.roots)
    allowed = allowed or (kind == "file" and path in policy.files)
    if not allowed or _overlap(path, policy.state) or _overlap(path, policy.path):
        raise PromotionError(f"Target is not allowed: {path}")
    if not path.parent.is_dir():
        raise PromotionError(f"Target parent must already exist: {path.parent}")
    return path


def _fingerprints(policy: Policy) -> dict:
    return {str(path): {"entries": _manifest(path), "permissions": _permissions(path)} for path in policy.protected}


@contextmanager
def global_lock(policy: Policy):
    """Persistent inode/file, OS-held lock; never unlink or replace this file."""
    _safe_path(policy.state)
    policy.state.mkdir(parents=True, exist_ok=True)
    path = policy.state / "promotion.lock"
    _safe_path(path)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    locked = False
    try:
        if os.fstat(descriptor).st_size == 0:
            os.write(descriptor, b"\0")
        os.lseek(descriptor, 0, os.SEEK_SET)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            locked = True
        except OSError as exc:
            raise PromotionError("Another promotion operation holds the global lock") from exc
        yield
    finally:
        if locked:
            os.lseek(descriptor, 0, os.SEEK_SET)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _journal_path(policy: Policy, transaction: str) -> Path:
    if not TRANSACTION_ID.fullmatch(transaction):
        raise PromotionError("Invalid transaction identifier")
    path = policy.state / transaction / "journal.json"
    _safe_path(path)
    return path


def _save(policy: Policy, record: dict) -> None:
    _atomic_json(_journal_path(policy, record["id"]), record)


def _check_other_transactions(policy: Policy, transaction: str | None = None) -> None:
    for path in sorted(policy.state.iterdir()):
        if TRANSACTION_ID.fullmatch(path.name) and (path / "journal.json").exists():
            record = _read_json(path / "journal.json")
            _journal_header(record, path.name)
            if record.get("status") in UNRESOLVED and path.name != transaction:
                raise PromotionError(f"Recover unresolved transaction first: {path.name}")


def _snapshot_path(policy: Policy, record: dict, side: str, index: int) -> Path:
    return _journal_path(policy, record["id"]).parent / side / str(index)


def _check_protected_candidates(policy: Policy, target: Path, candidate: Path | None, before: dict, after: dict) -> None:
    for protected in policy.protected:
        if _within(protected, target):
            actual = _manifest(protected)
            proposed = _manifest(candidate / protected.relative_to(target)) if candidate else {}
            if actual != proposed:
                raise PromotionError(f"Candidate changes a protected path: {protected}")
        elif _within(target, protected) and before != after:
            raise PromotionError(f"Target is inside a protected path: {protected}")


def prepare(policy: Policy, request_path: str | Path) -> dict:
    request = _read_json(_path(str(request_path)))
    _object(request, {"version", "eligibility", "targets"}, {"version", "eligibility", "targets"})
    if type(request["version"]) is not int or request["version"] != 1:
        raise PromotionError("Unsupported request version")
    eligibility = _object(request["eligibility"], {"class", "evidence"}, {"class", "evidence"})
    _enum(eligibility["class"], CLASSES, "eligibility class")
    evidence = _path(eligibility["evidence"])
    if not evidence.is_file() or _checkout(evidence):
        raise PromotionError("Evidence must be an existing file outside Git checkouts")
    if not isinstance(request["targets"], list) or not request["targets"]:
        raise PromotionError("At least one target is required")
    targets = []
    for item in request["targets"]:
        _object(item, {"path", "candidate", "kind"}, {"path", "candidate"})
        kind = item.get("kind", "directory")
        target = _target_path(policy, item["path"], kind)
        candidate = _path(item["candidate"]) if item["candidate"] is not None else None
        if candidate is None and kind != "file":
            raise PromotionError("Only file targets support a null deletion candidate")
        if candidate and (_checkout(candidate) or _overlap(candidate, policy.state)):
            raise PromotionError("Candidates must be outside checkouts and transaction state")
        targets.append((target, candidate, kind))
    for index, (target, candidate, _) in enumerate(targets):
        if any(_overlap(target, other[0]) for other in targets[:index]):
            raise PromotionError("Managed targets must not overlap")
        if any(other[1] and _overlap(target, other[1]) for other in targets) or _overlap(target, evidence):
            raise PromotionError("Candidates and evidence must not overlap managed targets")
    # Snapshot readers cooperate with publishers; normal agent reads are not locked.
    with global_lock(policy):
        _check_other_transactions(policy)
        transaction = uuid.uuid4().hex
        folder = policy.state / transaction
        folder.mkdir(mode=0o700 if os.name != "nt" else 0o777)
        protected = _fingerprints(policy)
        evidence_manifest = _manifest(evidence)
        _copy_snapshot(evidence, folder / "evidence", evidence_manifest)
        record = {"version": JOURNAL_VERSION, "platform": os.name, "id": transaction, "status": "prepared",
                  "policy": str(policy.path), "policy_sha256": policy.fingerprint,
                  "protected": protected, "eligibility": {"class": eligibility["class"],
                  "evidence": str(evidence), "manifest": evidence_manifest},
                  "targets": [], "operations": [], "staging": [], "publication_temps": [], "conflicts": []}
        for index, (target, candidate, kind) in enumerate(targets):
            before, after = _manifest(target), _manifest(candidate) if candidate else {}
            for manifest in (before, after):
                _validate_manifest(manifest)
                _supported_directory_modes(manifest)
            permissions = _permissions(target, before)
            parent_dacl = _dacl(target.parent)
            if before and before[""]["kind"] != kind:
                raise PromotionError(f"Target kind differs from declared kind: {target}")
            if candidate and (not after or after[""]["kind"] != kind):
                raise PromotionError(f"Candidate kind differs from declared kind: {candidate}")
            _check_protected_candidates(policy, target, candidate, before, after)
            _copy_snapshot(target, folder / "baseline" / str(index), before)
            if candidate:
                _copy_snapshot(candidate, folder / "candidate" / str(index), after)
            if permissions != _permissions(target) or parent_dacl != _dacl(target.parent):
                raise PromotionError(f"Target permissions changed during preparation: {target}")
            record["targets"].append({"path": str(target), "kind": kind, "baseline": before, "candidate": after,
                                      "baseline_permissions": permissions, "parent_dacl": parent_dacl,
                                      "ancestor_modes": _ancestor_modes(target)})
        _validate_operations(_plan(record))
        if protected != _fingerprints(policy) or policy.fingerprint != _digest(policy.path):
            raise PromotionError("Protected policy changed during preparation")
        _save(policy, record)
        return _summary(policy, record)


def _load(policy: Policy, transaction: str, *, inspection: bool = False) -> dict:
    record = _read_json(_journal_path(policy, transaction))
    _journal_header(record, transaction)
    if record["version"] != JOURNAL_VERSION:
        raise PromotionError("Legacy journals require their original trusted helper; directory modes cannot be inferred")
    fields = {"version", "platform", "id", "status", "policy", "policy_sha256", "protected", "eligibility", "targets", "operations", "staging", "publication_temps", "conflicts", "error"}
    _object(record, fields, fields - {"error"})
    if record["platform"] != os.name or record["policy"] != str(policy.path):
        raise PromotionError("Transaction identity or policy differs")
    for name in ("targets", "operations", "staging", "publication_temps", "conflicts"):
        if not isinstance(record[name], list):
            raise PromotionError(f"Invalid transaction {name}")
    if any(not isinstance(value, str) for value in record["conflicts"]) or ("error" in record and not isinstance(record["error"], str)):
        raise PromotionError("Invalid transaction diagnostics")
    if not isinstance(record["protected"], dict):
        raise PromotionError("Invalid protected fingerprints")
    if not inspection and (record["policy_sha256"] != policy.fingerprint or record["protected"] != _fingerprints(policy)):
        raise PromotionError("Protected policy/helper/evaluation material changed; no managed writes permitted")
    if not record["targets"]:
        raise PromotionError("Invalid transaction targets")
    paths = []
    for index, item in enumerate(record["targets"]):
        target_fields = {"path", "kind", "baseline", "candidate", "baseline_permissions", "parent_dacl", "ancestor_modes"}
        _object(item, target_fields, target_fields)
        target = _target_path(policy, item["path"], item["kind"])
        if any(_overlap(target, other) for other in paths):
            raise PromotionError("Transaction targets overlap")
        paths.append(target)
        for side in ("baseline", "candidate"):
            _validate_manifest(item[side])
            _supported_directory_modes(item[side])
            if _manifest(_snapshot_path(policy, record, side, index)) != item[side]:
                raise PromotionError(f"Frozen {side} snapshot changed: {index}")
        if not isinstance(item["baseline_permissions"], dict) or (os.name == "nt" and set(item["baseline_permissions"]) != set(item["baseline"])):
            raise PromotionError("Invalid baseline permission manifest")
        if any(not isinstance(value, str) for value in item["baseline_permissions"].values()) or (item["parent_dacl"] is not None and not isinstance(item["parent_dacl"], str)):
            raise PromotionError("Invalid recorded DACL")
        _mode_guards(item["ancestor_modes"])
        expected_ancestors = {str(parent) for parent in target.parents} if os.name != "nt" else set()
        if set(item["ancestor_modes"]) != expected_ancestors:
            raise PromotionError("Invalid target ancestor guards")
        if not inspection:
            _check_protected_candidates(policy, target, _snapshot_path(policy, record, "candidate", index), item["baseline"], item["candidate"])
    eligibility = _object(record["eligibility"], {"class", "evidence", "manifest"}, {"class", "evidence", "manifest"})
    _enum(eligibility["class"], CLASSES, "frozen eligibility class")
    _path(eligibility["evidence"])
    _validate_manifest(eligibility["manifest"])
    if _manifest(_journal_path(policy, transaction).parent / "evidence") != eligibility["manifest"]:
        raise PromotionError("Frozen eligibility evidence changed")
    # Plans are derived from frozen snapshots; a journal cannot introduce new writes.
    expected = _plan(record)
    if record["operations"]:
        if len(record["operations"]) != len(expected):
            raise PromotionError("Invalid operation journal")
        for actual, wanted in zip(record["operations"], expected):
            _object(actual, set(wanted) | {"state", "after_dacl"}, set(wanted) | {"state", "after_dacl"})
            _enum(actual["state"], OPERATION_STATES, "operation state")
            if type(actual["target"]) is not int or {key: actual[key] for key in wanted} != wanted:
                raise PromotionError("Journal operation differs from frozen snapshots")
            if actual["after_dacl"] is not None and not isinstance(actual["after_dacl"], str):
                raise PromotionError("Invalid operation DACL")
    for item in record["staging"]:
        _object(item, {"target", "path"}, {"target", "path"})
        if type(item["target"]) is not int or not 0 <= item["target"] < len(record["targets"]):
            raise PromotionError("Invalid staging target")
        path = _path(item["path"])
        base = _staging_base(Path(record["targets"][item["target"]]["path"]))
        if path.parent != base or not path.name.startswith(f".skill-promotion-{transaction}-"):
            raise PromotionError("Staging cleanup escaped its recorded temporary location")
    for item in record["publication_temps"]:
        _object(item, {"operation", "phase"}, {"operation", "phase"})
        if type(item["operation"]) is not int or not 0 <= item["operation"] < len(record["operations"]):
            raise PromotionError("Invalid publication temporary record")
        _enum(item["phase"], {"apply", "recover"}, "publication phase")
    return record


def _depth(relative: str) -> int:
    return len(relative.split("/")) if relative else 0


def _ancestor_modes(target: Path) -> dict:
    if os.name == "nt":
        return {}
    result = {}
    for parent in target.parents:
        entry = _entry(parent)
        if not entry or entry["kind"] != "directory":
            raise PromotionError(f"Ancestor is not a directory: {parent}")
        result[str(parent)] = entry["mode"]
    return result


def _check_mode_guards(guards: dict) -> None:
    for name, mode in guards.items():
        entry = _entry(Path(name))
        if not entry or entry["kind"] != "directory" or entry.get("mode") != mode:
            raise PromotionError(f"Ancestor mode changed; subtree preserved: {name}")


def _plan(record: dict) -> list[dict]:
    operations = []
    posix = record["platform"] != "nt"
    for index, target in enumerate(record["targets"]):
        before, after = target["baseline"], target["candidate"]
        current = dict(before)
        root = Path(target["path"])

        def append(relative, old, new):
            guards = {}
            if posix:
                path = root / relative if relative else root
                for parent in path.parents:
                    if _within(parent, root):
                        key = parent.relative_to(root).as_posix() if parent != root else ""
                        guards[str(parent)] = current[key]["mode"]
                    else:
                        guards[str(parent)] = target["ancestor_modes"][str(parent)]
            operations.append({"target": index, "path": relative, "before": old, "after": new,
                               "before_dacl": target["baseline_permissions"].get(relative) if old else None,
                               "ancestor_modes": guards})
            if new is None:
                current.pop(relative, None)
            else:
                current[relative] = new

        order = lambda value: (_depth(value), value)
        if posix:
            changed = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
            for key in sorted(before, key=order):
                entry = before[key]
                affected = any(key == "" or child == key or child.startswith(key + "/") for child in changed)
                if entry["kind"] != "directory" or not affected:
                    continue
                candidate = after.get(key)
                mode = (0o700 | (entry["mode"] & candidate["mode"] & 0o077)
                        if candidate and candidate["kind"] == "directory" else entry["mode"] | 0o700)
                if mode != entry["mode"]:
                    append(key, entry, {"kind": "directory", "mode": mode})

        removed = [key for key, entry in before.items() if key not in after or entry["kind"] != after[key]["kind"]]
        for key in sorted(removed, key=order, reverse=True):
            append(key, current[key], None)
        for key in sorted(after, key=order):
            old, new = current.get(key), after[key]
            if posix and new["kind"] == "directory":
                if old is None:
                    append(key, None, {"kind": "directory", "mode": 0o700})
            elif old != new:
                append(key, old, new)
        if posix:
            for key in sorted(after, key=order, reverse=True):
                if after[key]["kind"] == "directory" and current[key] != after[key]:
                    append(key, current[key], after[key])
    return operations


def _validate_operations(operations: list[dict]) -> None:
    if os.name != "nt":
        return
    # Replacing/deleting a read-only Windows file needs a separate attribute
    # mutation. V1 does not journal that intermediate state, so disallow it.
    for operation in operations:
        for side in ("before", "after"):
            entry = operation[side]
            if entry and entry["kind"] == "file" and not entry["mode"] & stat.S_IWRITE:
                raise PromotionError("Windows read-only file changes are unsupported; unchanged read-only members are allowed")


def _staging_base(target: Path) -> Path:
    base = target.parent
    while checkout := _checkout(base):
        if checkout.parent == checkout:
            raise PromotionError("No staging location outside the checkout")
        base = checkout.parent
    _safe_path(base)
    if base.stat().st_dev != target.parent.stat().st_dev:
        raise PromotionError("No same-volume staging location outside the checkout")
    return base


def _clean_staging(policy: Policy, record: dict) -> None:
    for item in record["staging"]:
        _object(item, {"target", "path"}, {"target", "path"})
        index = item["target"]
        if type(index) is not int or not 0 <= index < len(record["targets"]):
            raise PromotionError("Invalid staging target")
        path = _path(item["path"])
        base = _staging_base(Path(record["targets"][index]["path"]))
        if path.parent != base or not path.name.startswith(f".skill-promotion-{record['id']}-"):
            raise PromotionError("Staging cleanup escaped its recorded temporary location")
        if path.exists():
            _manifest(path)  # Reject links before recursively removing this owned stage.
            _writable_stage(path)
            def remove_readonly(function, failed, _error):
                failed = _path(str(failed))
                if not _within(failed, path) or not failed.is_file():
                    raise PromotionError(f"Cannot clean owned staging: {failed}")
                failed.chmod(stat.S_IREAD | stat.S_IWRITE)
                function(failed)
            shutil.rmtree(path, onerror=remove_readonly)


def _writable_stage(path: Path) -> None:
    """Change only owned disposable directories, never frozen snapshots or targets."""
    if os.name != "nt":
        manifest = _manifest(path)
        for relative in sorted(manifest, key=_depth):
            if manifest[relative]["kind"] == "directory":
                (path / relative if relative else path).chmod(0o700)


def _publication_path(record: dict, operation_index: int, phase: str) -> Path:
    operation = record["operations"][operation_index]
    root = Path(record["targets"][operation["target"]]["path"])
    path = root / operation["path"] if operation["path"] else root
    return path.parent / f".skill-publish-{record['id']}-{operation_index}-{phase}.tmp"


def _prepare_publication(policy: Policy, record: dict, index: int, phase: str,
                         entry: dict, source: Path | None, saved_dacl: str | None) -> Path:
    path = _publication_path(record, index, phase)
    _safe_path(path)
    if path.exists():
        raise PromotionError(f"Publication temporary path already exists: {path}")
    record["publication_temps"].append({"operation": index, "phase": phase})
    _save(policy, record)  # A crash after CREATE_NEW still has an owned recovery path.
    if entry["kind"] == "directory":
        path.mkdir()  # Default mode inherits this actual destination parent's DACL.
    else:
        _native_publication_file(source, path, saved_dacl)
    if saved_dacl is not None:
        _set_dacl(path, saved_dacl)
    if _entry(path) != entry:
        raise PromotionError(f"Publication temporary differs from expected content: {path}")
    return path


def _clean_publications(record: dict) -> None:
    for item in record["publication_temps"]:
        _object(item, {"operation", "phase"}, {"operation", "phase"})
        if type(item["operation"]) is not int or not 0 <= item["operation"] < len(record["operations"]) or item["phase"] not in {"apply", "recover"}:
            raise PromotionError("Invalid publication temporary record")
        path = _publication_path(record, item["operation"], item["phase"])
        if os.path.lexists(path):
            _safe_path(path)
            path.rmdir() if path.is_dir() else path.unlink()


def _expected_permissions(record: dict, index: int) -> dict:
    result = dict(record["targets"][index]["baseline_permissions"])
    if os.name == "nt":
        for operation in record["operations"]:
            if operation["target"] == index:
                if operation["after"] is None:
                    result.pop(operation["path"], None)
                else:
                    result[operation["path"]] = operation["after_dacl"]
    return result


def _write_entry(path: Path, before, after, source: Path | None,
                 before_dacl: str | None = None, after_dacl: str | None = None) -> None:
    if _entry(path) != before or _dacl(path) != before_dacl:
        raise PromotionError(f"Concurrent target change: {path}")
    if after is None:
        path.rmdir() if before["kind"] == "directory" else path.unlink()
    elif after["kind"] == "directory" and os.name != "nt":
        if before is None:
            path.mkdir(mode=0o700)
        path.chmod(after["mode"])
    else:
        if source is None or _entry(source) != after:
            raise PromotionError(f"Staged file differs from expected bytes: {path}")
        _safe_path(path.parent)
        if source.stat().st_dev != path.parent.stat().st_dev:
            raise PromotionError(f"Cross-volume file replacement is not supported: {path}")
        os.replace(source, path)
    if _entry(path) != after or _dacl(path) != after_dacl:
        raise PromotionError(f"Post-write verification failed: {path}")


def apply(policy: Policy, transaction: str, *, _fault: Callable | None = None) -> dict:
    with global_lock(policy):
        _check_other_transactions(policy, transaction)
        record = _load(policy, transaction)
        if record["status"] != "prepared":
            raise PromotionError("Only a prepared transaction can be applied; inspect/recover existing work")
        _validate_operations(_plan(record))
        for target in record["targets"]:
            path = Path(target["path"])
            _check_mode_guards(target["ancestor_modes"])
            if (_manifest(path) != target["baseline"] or _permissions(path) != target["baseline_permissions"]
                    or _dacl(path.parent) != target["parent_dacl"]):
                raise PromotionError(f"Baseline changed: {target['path']}")
        stages = []
        try:
            for index, target in enumerate(record["targets"]):
                stage = Path(tempfile.mkdtemp(prefix=f".skill-promotion-{transaction}-", dir=_staging_base(Path(target["path"]))))
                record["staging"].append({"target": index, "path": str(stage)})
                _save(policy, record)
                _copy_snapshot(_snapshot_path(policy, record, "candidate", index), stage / "candidate", target["candidate"])
                _writable_stage(stage)
                stages.append(stage / "candidate")
            # A complete second preflight after staging precedes all managed writes.
            _load(policy, transaction)
            for target in record["targets"]:
                path = Path(target["path"])
                _check_mode_guards(target["ancestor_modes"])
                if (_manifest(path) != target["baseline"] or _permissions(path) != target["baseline_permissions"]
                        or _dacl(path.parent) != target["parent_dacl"]):
                    raise PromotionError(f"Baseline changed during staging: {target['path']}")
            record["operations"] = [dict(operation, state="pending", after_dacl=None) for operation in _plan(record)]
            record["status"] = "applying"
            _save(policy, record)
            for index, operation in enumerate(record["operations"]):
                operation["state"] = "intent"
                _save(policy, record)
                if _fault:
                    _fault("before_write", index, record)
                _check_mode_guards(operation["ancestor_modes"])
                root = Path(record["targets"][operation["target"]]["path"])
                path = root / operation["path"] if operation["path"] else root
                source = stages[operation["target"]] / operation["path"] if operation["path"] else stages[operation["target"]]
                if os.name == "nt" and operation["after"]:
                    source = _prepare_publication(policy, record, index, "apply", operation["after"], source,
                                                  operation["before_dacl"] if operation["before"] else None)
                    operation["after_dacl"] = _dacl(source)
                    _save(policy, record)
                    if _fault:
                        _fault("after_publication_stage", index, record)
                _write_entry(path, operation["before"], operation["after"], source,
                             operation["before_dacl"], operation["after_dacl"])
                if _fault:
                    _fault("after_write", index, record)
                operation["state"] = "done"
                _save(policy, record)
            for index, target in enumerate(record["targets"]):
                path = Path(target["path"])
                if _manifest(path) != target["candidate"] or _permissions(path) != _expected_permissions(record, index):
                    raise PromotionError(f"Complete package verification failed: {target['path']}")
            if record["protected"] != _fingerprints(policy):
                raise PromotionError("Protected material changed during publication")
            record["status"] = "applied"
            _save(policy, record)
        except Exception as exc:
            if record["status"] == "applying":
                record["status"] = "interrupted"
                record["error"] = str(exc)
                _save(policy, record)
            raise PromotionError(f"Publication stopped: {exc}") from exc
        finally:
            _clean_publications(record)
            _clean_staging(policy, record)
        return _summary(policy, record)


def recover(policy: Policy, transaction: str, *, _fault: Callable | None = None) -> dict:
    with global_lock(policy):
        _check_other_transactions(policy, transaction)
        record = _load(policy, transaction)
        if record["status"] in {"recovered", "cancelled"}:
            result = status(policy, transaction)
            result[f"already_{record['status']}"] = True
            return result
        if record["status"] == "prepared" and not record["operations"]:
            _clean_staging(policy, record)
            record["status"] = "cancelled"
            _save(policy, record)
            return _summary(policy, record)
        record["status"] = "recovering"
        record["conflicts"] = []
        conflicted_paths = []
        _save(policy, record)
        _clean_publications(record)
        for index in reversed(range(len(record["operations"]))):
            operation = record["operations"][index]
            if operation["state"] in {"pending", "undone"}:
                continue
            root = Path(record["targets"][operation["target"]]["path"])
            path = root / operation["path"] if operation["path"] else root
            try:
                _check_mode_guards(operation["ancestor_modes"])
                current = _entry(path)
                current_dacl = _dacl(path)
                if current != operation["before"] or current_dacl != operation["before_dacl"]:
                    if current != operation["after"] or current_dacl != operation["after_dacl"]:
                        raise PromotionError(f"External edits preserved: {path}")
                    old, new = operation["before"], operation["after"]
                    if old and new and old["kind"] == new["kind"] == "directory":
                        if any(_within(failed, path) for failed in conflicted_paths):
                            raise PromotionError(f"Descendant recovery conflict; directory mode preserved: {path}")
                        if "mode" in old and old["mode"] & ~new["mode"] & 0o077:
                            # Do not expose an unexpected file or a later edit to an
                            # already-restored child when restoring a broader mode.
                            prefix = operation["path"] + "/" if operation["path"] else ""
                            baseline = record["targets"][operation["target"]]["baseline"]
                            expected = {key[len(prefix):]: entry for key, entry in baseline.items()
                                        if key.startswith(prefix)}
                            expected[""] = new
                            if _manifest(path) != expected:
                                raise PromotionError(f"Changed subtree preserved before directory mode restoration: {path}")
                    operation["state"] = "undo_intent"
                    _save(policy, record)
                    if _fault:
                        _fault("before_restore", index, record)
                    _check_mode_guards(operation["ancestor_modes"])
                    source = None
                    temporary = None
                    try:
                        if os.name == "nt" and operation["before"]:
                            snapshot = _snapshot_path(policy, record, "baseline", operation["target"])
                            source = _prepare_publication(policy, record, index, "recover", operation["before"],
                                                          snapshot / operation["path"] if operation["path"] else snapshot,
                                                          operation["before_dacl"])
                        elif operation["before"] and operation["before"]["kind"] == "file":
                            temporary = tempfile.TemporaryDirectory(prefix=f".skill-restore-{transaction}-", dir=_staging_base(root))
                            source = Path(temporary.name) / "entry"
                            snapshot = _snapshot_path(policy, record, "baseline", operation["target"])
                            _copy_file(snapshot / operation["path"] if operation["path"] else snapshot, source)
                        _write_entry(path, operation["after"], operation["before"], source,
                                     operation["after_dacl"], operation["before_dacl"])
                    finally:
                        _clean_publications(record)
                        if temporary:
                            temporary.cleanup()
                    if _fault:
                        _fault("after_restore", index, record)
                operation["state"] = "undone"
            except (PromotionError, OSError) as exc:
                operation["state"] = "conflicted"
                conflicted_paths.append(path)
                record["conflicts"].append(str(exc))
            _save(policy, record)
        for target in record["targets"]:
            try:
                path = Path(target["path"])
                if _manifest(path) != target["baseline"] or _permissions(path) != target["baseline_permissions"]:
                    record["conflicts"].append(f"Target does not match baseline: {target['path']}")
            except (PromotionError, OSError) as exc:
                record["conflicts"].append(str(exc))
        record["status"] = "conflicted" if record["conflicts"] else "recovered"
        _save(policy, record)
        _clean_publications(record)
        _clean_staging(policy, record)
        return _summary(policy, record)


def _summary(policy: Policy, record: dict) -> dict:
    return {"transaction": record["id"], "status": record["status"],
            "journal": str(_journal_path(policy, record["id"])), "conflicts": record["conflicts"]}


def status(policy: Policy, transaction: str | None = None):
    if transaction:
        record = _read_json(_journal_path(policy, transaction))
        _journal_header(record, transaction)
        if record["version"] != JOURNAL_VERSION:
            return {"transaction": transaction, "status": record["status"],
                    "journal": str(_journal_path(policy, transaction)), "policy": record["policy"],
                    "policy_sha256": record["policy_sha256"], "inspection_requires_original_helper": True}
        if record.get("policy") != str(policy.path) or record.get("policy_sha256") != policy.fingerprint:
            # A shared lock/state directory can contain older or separately
            # authorized policies. Listing them grants no access to their targets.
            return {"transaction": transaction, "status": record["status"],
                    "journal": str(_journal_path(policy, transaction)),
                    "policy": record.get("policy"), "policy_sha256": record.get("policy_sha256"),
                    "inspection_requires_recorded_policy": True}
        record = _load(policy, transaction, inspection=True)
        result = _summary(policy, record)
        result["protected_match"] = record["policy_sha256"] == policy.fingerprint and record["protected"] == _fingerprints(policy)
        result["targets"] = []
        for index, target in enumerate(record["targets"]):
            path = _target_path(policy, target["path"], target["kind"])
            actual = _manifest(path)
            permissions = _permissions(path)
            result["targets"].append({"path": str(path), "matches_baseline": actual == target["baseline"], "matches_candidate": actual == target["candidate"],
                                      "permissions_match_baseline": permissions == target["baseline_permissions"],
                                      "permissions_match_candidate": permissions == _expected_permissions(record, index)})
        return result
    if not policy.state.exists():
        return []
    return [status(policy, path.name) for path in sorted(policy.state.iterdir())
            if TRANSACTION_ID.fullmatch(path.name) and (path / "journal.json").exists()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "apply", "status", "recover"))
    parser.add_argument("--policy", required=True)
    parser.add_argument("--request")
    parser.add_argument("--transaction")
    args = parser.parse_args(argv)
    try:
        policy = load_policy(args.policy)
        if args.command == "prepare":
            if not args.request or args.transaction:
                raise PromotionError("prepare requires --request and does not accept --transaction")
            result = prepare(policy, args.request)
        else:
            if args.request or (args.command != "status" and not args.transaction):
                raise PromotionError("apply/recover require --transaction; --request is prepare-only")
            result = globals()[args.command](policy, args.transaction)
        print(json.dumps(result, indent=2))
        return 2 if isinstance(result, dict) and result.get("status") == "conflicted" else 0
    except (PromotionError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
