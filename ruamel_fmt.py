#!/usr/bin/env python3

# https://stackoverflow.com/a/31005595/1872036

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


def main():
    # I'm sorry, Jon.
    # https://linuxpip.org/broken-pipe-python-error/
    # Ignore SIG_PIPE and don't throw exceptions on it...
    # http://docs.python.org/library/signal.html
    signal(SIGPIPE, SIG_DFL)
    # Read from stdin if no file provided
    data = Path(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    # FIXME Add a proper RC here
    process_document(data)


if __name__ == "__main__":
    main()
