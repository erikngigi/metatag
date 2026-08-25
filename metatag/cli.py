"""CLI Schema and Input Validaition Module.

Configures terminal flags for interactive wizard launch, dry-run mode, and version checking.
"""

import argparse
import sys

import argcomplete

from metatag import __version__


def parse_arguments() -> argparse.Namespace:
    """
    Configures the CLI argument schema and parses terminal inputs.
    """
    parser = argparse.ArgumentParser(
        prog="metatag",
        description="A structured, API-driven renaming engine that standardizes "
        "messy TV show and Anime file collections using remote metadata databases.",
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        dest="interactive",
        help="Launch step-by-step interactive configuration setup wizard",
    )

    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        dest="preview",
        help="Perform a dry run. Display proposed filename changes without altering files on disk.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the application version and exit.",
    )

    # Register the autocomplete hook before calling parse_args()
    argcomplete.autocomplete(parser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()
