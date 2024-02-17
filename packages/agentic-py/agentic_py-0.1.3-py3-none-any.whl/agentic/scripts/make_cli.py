from typing import Callable, Tuple, Any
import argparse
from pathlib import Path
import inspect


def make_cli_and_get_args(name: str, func: Callable, args: Tuple[Any, ...]):
    """Takes a Python function and builds ArgumentParser instance using the
    function's signature.

    Returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog=name,
        add_help=False,
    )
    sig = inspect.signature(func)

    for param in sig.parameters.values():
        name = param.name
        parser.add_argument(name, nargs=1)

    parsed = parser.parse_args(args)
    as_vars = vars(parsed)
    return tuple(as_vars[key][0] for key in as_vars)
