#!/usr/bin/env python3

# https://stackoverflow.com/a/31005595/1872036

import argparse
import sys
from pathlib import Path
from signal import SIG_DFL, SIGPIPE, signal

import ruamel.yaml


def normalise(d):
    LT = ruamel.yaml.scalarstring.LiteralScalarString  # type: ignore
    if isinstance(d, dict):
        for k, v in d.items():
            d[k] = normalise(v)
        return d
    if isinstance(d, list):
        for idx, elem in enumerate(d):
            d[idx] = normalise(elem)
        return d
    if not isinstance(d, str):
        return d
    if "\n" in d:
        if isinstance(d, LT):
            return d  # already a block style literal scalar
        return LT(d)
    return str(d)


def process_document(data):
    yaml = ruamel.yaml.YAML()
    # ruamel wraps at around 80chars by default. Let's allow more.
    yaml.width = 4096  # type: ignore
    data = normalise(yaml.load(data))
    return yaml.dump(data, sys.stdout)


def read_input(path_arg):
    if path_arg == "-":
        return sys.stdin.read()
    return Path(path_arg).read_text()


def main(argv=None):
    # I'm sorry, Jon.
    # https://linuxpip.org/broken-pipe-python-error/
    # Ignore SIG_PIPE and don't throw exceptions on it...
    # http://docs.python.org/library/signal.html
    signal(SIGPIPE, SIG_DFL)

    parser = argparse.ArgumentParser(
        description="Format YAML documents for human readability."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="YAML file to format (default: stdin; use '-' for stdin)",
    )
    args = parser.parse_args(argv)

    try:
        data = read_input(args.input)
        process_document(data)
    except FileNotFoundError:
        print(f"ruamel-fmt: file not found: {args.input}", file=sys.stderr)
        return 1
    except ruamel.yaml.YAMLError as exc:  # type: ignore[attr-defined]
        print(f"ruamel-fmt: YAML error: {exc}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ruamel-fmt: unexpected error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
