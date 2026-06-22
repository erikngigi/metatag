"""Application Bootstrapper and Router.

Acts as the root orchestrator of the metatag application. Parses terminal
flags and conditionally hands off execution to the appropriate controller layer.
"""

from __future__ import annotations

import sys

from metatag.cli import parse_arguments
from metatag.controllers.api_presenter import APIMetadataController
from metatag.controllers.directory_selector import DirectoryController
from metatag.views.interactive import InteractiveWizard
from metatag.views.theme import Theme


def main() -> None:
    """Orchestrates system startup and conditional flag routing."""
    # 1. Parse incoming terminal flags via argparse
    args = parse_arguments()

    # 2. INTERACTIVE WIZARD PATHWAY
    if args.interactive:
        # Instantiate the View layer module
        wizard = InteractiveWizard()

        # Inject the View into the Controller layer module (Dependency Injection)
        api_controller = APIMetadataController(wizard)

        # Execute the controller logic pipeline
        api_controller.run()

        # ----------------------------------------------------------------------
        # Pipeline B: Local Folder Ingestion & Directory Selection
        # ----------------------------------------------------------------------
        print(f"\n{Theme.CYAN} ---Initializing Local Filesystem Setup--- {Theme.RESET}")

        # Inject the same view framework into your directory controller
        dir_controller = DirectoryController(wizard)

        target_dir = dir_controller.run()

        print(f"{Theme.CYAN}Selected Directory:{Theme.RESET} {Theme.GREEN}{target_dir}{Theme.RESET}")

        # Clean termination so it never falls through to old scanning processes
        sys.exit(0)

    # 3. FALLBACK DEFAULT LOGIC
    # Since positional arguments are currently disabled in cli.py, running
    # the application without any flags would cause it to silently do nothing.
    # This block provides a helpful message guiding users to the interactive flag.
    print(
        "Welcome to metatag!\n"
        "Standard file system mode is temporarily offline for maintenance.\n"
        "Please launch the interactive metadata explorer using:\n\n"
        "    $ metatag --interactive\n"
        "    $ metatag -a\n",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
