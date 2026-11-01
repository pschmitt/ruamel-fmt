# Agent guidance

`ruamel-fmt` is a Python command-line formatter for YAML, using `ruamel.yaml`.

## Development

- The CLI implementation is in `ruamel_fmt.py`; package metadata and dependencies are in `pyproject.toml` and `requirements.txt`.
- Use the Nix flake's development environment for local tooling. Preserve YAML semantics and comments when changing formatting behavior.
- Validate with disposable YAML fixtures; do not process files that may contain credentials.

## CI

- Before changing CI, inspect the current guidance in `pschmitt/ci-workflows`. Pin shared reusable workflow and action references to `@main`.
