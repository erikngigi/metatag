"""Workflow Automation and Pipeline Controller.

Acts as the Controller layer in the MVC architectural pattern. This module
orchestrates application lifecycle execution by consuming parsed arguments
from the CLI view, managing scanner configuration models, and controlling
terminal-facing output and execution states.
"""

import argparse
import sys

from metatag.models.scanner import FileScanner


class MediaRenamerController:
    """Coordinates core business logic execution pipelines for media processing."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

        self.scanner = FileScanner(
            target_dir=args.target_dir,
            recursive=args.recursive,
            videos_only=args.videos_only,
            subtitles_only=args.subtitles_only,
        )

    def run(self) -> None:
        """Executes the operational pipeline.

        Performs safety verification againist inputs paths, gathers discovered assests
        via the scanner component, and outputs formatted items directly to starnard
        stream handles.
        """
        if not self.scanner.is_valid_directory():
            print(f"Error: '{self.args.target_dir}' is not a valid directory", file=sys.stderr)
            sys.exit(1)

        files = self.scanner.scan_files()

        if not files:
            print("No matching files found based on your filters.")
            return

        for file in files:
            if self.args.recursive:
                print(f"{file.relative_to(self.scanner.target_dir)}")
            else:
                print(f"{file.name}")
