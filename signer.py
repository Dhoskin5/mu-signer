#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import os
import pexpect

def load_keymap(path):
    with open(path, "r") as f:
        return json.load(f)

def get_key_entry(keymap, key_id):
    if key_id not in keymap:
        raise KeyError(f"Key ID '{key_id}' not found in keymap.")
    return keymap[key_id]

def verify_manifest_key_id(manifest_path, expected_key_id):
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    manifest_key_id = manifest.get("key_id")
    if manifest_key_id != expected_key_id:
        raise ValueError(f"Manifest key_id '{manifest_key_id}' does not match expected key_id '{expected_key_id}'")

def sign_manifest(manifest_path, private_key_path, password):
    print(f"Signing with key: {private_key_path}")
    cmd = f"minisign -S -s {private_key_path} -m {manifest_path} -x {manifest_path}.minisig"

    child = pexpect.spawn(cmd, encoding="utf-8")

    try:
        child.expect("(?i)password:", timeout=5)  # case-insensitive match
        child.sendline(password)
        child.expect(pexpect.EOF)
    except pexpect.exceptions.EOF:
        print("minisign exited unexpectedly.")
        sys.exit(1)
    except pexpect.exceptions.TIMEOUT:
        print("minisign password prompt timeout.")
        sys.exit(1)

    if child.exitstatus != 0:
        print("Signing failed.")
        sys.exit(child.exitstatus)

def main():
    parser = argparse.ArgumentParser(description="Sign a manifest.json using a private key from keymap.json")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json")
    parser.add_argument("--keymap", required=True, help="Path to keymap.json")
    parser.add_argument("--key-id", required=True, help="Key ID to use for signing")
    parser.add_argument("--password", default="", help="Password for signing key (can be empty)")
    parser.add_argument("--key-dir", default=".", help="Directory containing private keys")

    args = parser.parse_args()

    manifest_path = args.manifest
    keymap = load_keymap(args.keymap)
    key_entry = get_key_entry(keymap, args.key_id)
    private_key_path = os.path.join(args.key_dir, key_entry["private_key"])

    verify_manifest_key_id(manifest_path, args.key_id)

    print(f"Signing manifest using key ID: {args.key_id}")
    sign_manifest(manifest_path, private_key_path, args.password)

    print(f"Output: {manifest_path}.minisig")

if __name__ == "__main__":
    main()

