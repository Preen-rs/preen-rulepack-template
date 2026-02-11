#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import tomllib


ROOT = pathlib.Path(__file__).resolve().parent.parent


def fail(msg: str) -> None:
    print(f"validation failed: {msg}", file=sys.stderr)
    raise SystemExit(1)


def parse_toml(path: pathlib.Path) -> dict:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"{path}: invalid TOML ({exc})")
    raise AssertionError("unreachable")


def non_empty_string(data: dict, key: str, path: pathlib.Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{path}: `{key}` must be a non-empty string")
    return value


def main() -> None:
    manifest_path = ROOT / "manifest.toml"
    signature_path = ROOT / "manifest.sig"
    certificate_path = ROOT / "manifest.cert"
    if not manifest_path.exists():
        fail("manifest.toml is missing")
    if not signature_path.exists():
        fail("manifest.sig is missing")
    if not certificate_path.exists():
        fail("manifest.cert is missing")

    manifest = parse_toml(manifest_path)
    if manifest.get("schema_version") != 1:
        fail("manifest.schema_version must be 1")
    if manifest.get("action_api") != 1:
        fail("manifest.action_api must be 1")

    non_empty_string(manifest, "pack_id", manifest_path)
    non_empty_string(manifest, "name", manifest_path)
    non_empty_string(manifest, "version", manifest_path)
    non_empty_string(manifest, "core_compat", manifest_path)

    rules = manifest.get("rules")
    if not isinstance(rules, list) or not rules:
        fail("manifest.rules must contain at least one rule")

    seen_ids: set[str] = set()
    for idx, rule_ref in enumerate(rules):
        if not isinstance(rule_ref, dict):
            fail(f"manifest.rules[{idx}] must be a table")
        rule_id = non_empty_string(rule_ref, "id", manifest_path)
        if rule_id in seen_ids:
            fail(f"duplicate rule id: {rule_id}")
        seen_ids.add(rule_id)
        rule_file = non_empty_string(rule_ref, "rule_file", manifest_path)
        rule_path = ROOT / rule_file
        if not rule_path.exists():
            fail(f"missing rule file: {rule_file}")
        rule = parse_toml(rule_path)
        if rule.get("schema_version") != 1:
            fail(f"{rule_file}: schema_version must be 1")
        if non_empty_string(rule, "id", rule_path) != rule_id:
            fail(f"{rule_file}: id must match manifest rule ref id `{rule_id}`")
        if "match" not in rule or not isinstance(rule["match"], dict):
            fail(f"{rule_file}: missing [match] table")
        if "action" not in rule or not isinstance(rule["action"], dict):
            fail(f"{rule_file}: missing [action] table")

    sig_content = signature_path.read_text(encoding="utf-8").strip()
    if not sig_content or sig_content == "REPLACE_WITH_SIGSTORE_SIGNATURE":
        fail("manifest.sig is placeholder; replace with a real Sigstore signature")
    cert_content = certificate_path.read_text(encoding="utf-8").strip()
    if not cert_content or cert_content == "REPLACE_WITH_SIGSTORE_CERTIFICATE":
        fail("manifest.cert is placeholder; replace with a real Sigstore certificate")

    print("rulepack validation passed")


if __name__ == "__main__":
    main()
