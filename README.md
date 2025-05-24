# mu-signer

A minimal, containerized signing utility using `minisign` and a structured `keymap.json`.

## Overview

This tool is designed to run in a container and sign files based on a JSON-based key map.
It supports signing workflows in both local and CI environments.

## Files

- `signer.py` — main signing logic (Python)
- `Dockerfile` — container definition
- `build.sh` / `clean.sh` — helper scripts
- `keymap.template.json` — sample key mapping format

## Security Note

**Do not commit `keymap.json`** — this may contain sensitive or environment-specific signing key paths.

## Setup

1. Create your own `keymap.json` from the template:
    ```bash
    cp keymap.template.json keymap.json
    ```

2. Edit it to reference your real `.minisign.key` files and key IDs.

3. Build the container:
    ```bash
    ./build.sh
    ```

4. Run it:
    ```bash
    docker run --rm -v $PWD:/signer mu-signer:latest <args>
    ```

## Signing Format

Each entry in `keymap.json` should follow:

```json
{
  "my-key-name": {
    "key_id": "ABCD1234",
    "private_key_path": "/absolute/path/to/key",
    "description": "Describe this key",
    "expires": "YYYY-MM-DD"
  }
}
```
