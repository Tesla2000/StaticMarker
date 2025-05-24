from __future__ import annotations

from pathlib import Path

from .config import Config
from .config import create_config_with_args
from .config import parse_arguments
from .transaction import transation
from .transform.modify_file import modify_file


def main() -> int:
    """
    The `main` function processes a list of filenames from a configuration,
    filtering for Python files, and applies a modification function to each,
    returning a failure status indicating whether any modifications failed. It
    utilizes argument parsing and configuration creation to determine the files
    to be modified.
    :return: An integer indicating the success (0) or failure (1) of file
    modifications.
    """
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    with transation(config.pos_args):
        return _main(config)


def _main(config: Config) -> int:
    paths = tuple(map(Path, config.pos_args))
    fail = 0
    run = 1
    while run:
        run = 0
        for filepath in filter(lambda path: path.suffix == ".py", paths):
            modified = modify_file(filepath, config=config)
            run |= modified
            fail |= modified
    return fail
