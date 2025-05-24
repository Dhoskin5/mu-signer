#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import argparse
from pathlib import Path

def load_keymap(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_key_entry(keymap, key_id=None):
    if key_id:
        return key_id, keymap[key_id]
    # Use first key as default
    first_id = next(iter(keymap))
    return first_id, keymap[first_id]

def sign_manifest(manifest_path, private_key_path):
    result = subprocess.run([
        "minisign",
        "-S",
        "-s", private_key_path,
        "-m", manifest_path,
        "-x", "manifest.signed.json.minisig"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Signing failed:", result.stderr)
        sys.exit(1)

def extract_key_id(sigfile):
    with open(sigfile, 'r') as f:
        for line in f:
            if line.startswith("untrusted comment:"):
                return line.strip().split()[-1]
    raise RuntimeError("Unable to extract key ID")

def inject_key_id(manifest_path, key_id, output_path):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    manifest["key_id"] = key_id
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Sign a manifest.json using a private key from keymap.json")
    parser.add_argument("--manifest", default="manifest.json", help="Path to manifest.json")
    parser.add_argument("--keymap", default="keymap.json", help="Path to keymap.json")
    parser.add_argument("--key-id", help="Key ID to use (defaults to first in keymap)")
    args = parser.parse_args()

    keymap = load_keymap(args.keymap)
    key_id, key_entry = get_key_entry(keymap, args.key_id)
    manifest_path = args.manifest

    print(f"Signing manifest with key ID: {key_id}")

    sign_manifest(manifest_path, os.path.expanduser(key_entry["private_key"]))
    injected_manifest = "manifest.signed.json"
    inject_key_id(manifest_path, key_id, injected_manifest)
    
    actual_id = extract_key_id("manifest.signed.json.minisig")
    if actual_id != key_id:
        raise RuntimeError(f"Key ID mismatch! Expected {key_id}, got {actual_id}")

    print(f"Output: {injected_manifest}, manifest.signed.json.minisig")

if __name__ == "__main__":
    main()

