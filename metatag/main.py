"""Application Bootstrapper and Router.

Acts as the root orchestrator of the metatag application. Parses terminal
flags and conditionally hands off execution to the appropriate controller layer.
"""

from __future__ import annotations

import sys

from metatag.cli import parse_arguments
from metatag.controllers.api_selector import APISelectorController
from metatag.controllers.directory_selector import DirectoryController
from metatag.controllers.file_selector import FileSelectorController
from metatag.controllers.renamer import FileRenamerController
from metatag.models.tvmaze_model import TVMazeModel
from metatag.views.interactive import InteractiveWizard
from metatag.views.theme import Theme


def main() -> None:
    """Orchestrates system startup and conditional flag routing."""
    # 1. Parse incoming terminal flags via argparse
    args = parse_arguments()

    # 2. INTERACTIVE WIZARD PATHWAY
    if args.interactive:
        # 1. Instantiate the Model layer module (Data Engine)
        tvmaze = TVMazeModel()

        # 2. Instantiate the View layer module (User Interface)
        wizard = InteractiveWizard()

        while True:
            try:
                # Inject the View into the Controller layer module (Dependency Injection)
                api_controller = APISelectorController(wizard=wizard, tvmaze=tvmaze)

                # Execute the controller logic pipeline (Returns exact types needed)
                show_title, season_num, season_episode_list = api_controller.run()

                # ----------------------------------------------------------------------
                # Pipeline B: Local Folder Ingestion & Directory Selection
                # ----------------------------------------------------------------------
                dir_controller = DirectoryController(wizard)
                target_dir = dir_controller.run()

                # ----------------------------------------------------------------------
                # Pipeline C: Target File Filtering and Inventory List Extraction
                # ----------------------------------------------------------------------
                file_controller = FileSelectorController(wizard, target_dir)
                files_to_process = file_controller.run()

                # ----------------------------------------------------------------------
                # Pipeline D: File System Execution Sequence
                # ----------------------------------------------------------------------
                # ----------------------------------------------------------------------
                if files_to_process:
                    renamer = FileRenamerController(
                        target_dir=target_dir, local_files=files_to_process, remote_episodes=season_episode_list
                    )

                renamer.execute_rename(show_name=show_title, season_num=season_num, dry_run=True)

                if wizard.prompt_rename_confirmation():
                    renamer.execute_rename(show_name=show_title, season_num=season_num, dry_run=args.dry_run)
                else:
                    print(f"{Theme.YELLOW}Renaming sequence aborted by user. No files were changed.{Theme.RESET}")

                next_move = wizard.prompt_post_rename_options()

                if next_move == "exit":
                    print(f"{Theme.GREEN}Exiting Metatag. Goodbye.{Theme.RESET}")
                    break

                wizard.clear_screen()

            except KeyboardInterrupt:
                print(f"{Theme.YELLOW}Execution interrupted by user. Exiting Metatag.")
                break

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
