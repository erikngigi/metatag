"""Application Bootstrapper and Router.

Acts as the root orchestrator of the metatag application. Parses terminal
flags and conditionally hands off execution to the appropriate controller layer.
"""

from __future__ import annotations

import sys

from metatag.cli import parse_arguments
from metatag.colors import colors, cprint
from metatag.controllers.api_selector import APISelectorController
from metatag.models.anime_model import AnimeJikanModel
from metatag.models.tvmaze_model import TVMazeModel
from metatag.views.anime_menu import AnimeMenuView
from metatag.views.base_menu import BaseMenuView
from metatag.views.tv_menu import TVMenuView


def main() -> None:
    """Orchestrates system startup and conditional flag routing."""
    # 1. Parse incoming terminal flags via argparse
    args = parse_arguments()

    # 2. INTERACTIVE WIZARD PATHWAY
    if args.interactive:
        # 1. Instantiate the Model layer module (Data Engine)
        anime = AnimeJikanModel()
        tvmaze = TVMazeModel()

        # 2. Instantiate the View layer module (User Interface)
        base_menu = BaseMenuView()
        anime_menu = AnimeMenuView()
        tvmenu = TVMenuView()

        while True:
            try:
                # Inject the View into the Controller layer module (Dependency Injection)
                api_controller = APISelectorController(
                    base_menu=base_menu, anime=anime, anime_menu=anime_menu, tvmaze=tvmaze, tvmenu=tvmenu
                )

                api_controller.run(args)

                next_move = base_menu.prompt_post_rename_options()

                if next_move == "exit":
                    cprint(colors.YELLOW, "Exiting Metatag. Goodbye.")
                    break

                base_menu.clear_screen()

            except KeyboardInterrupt:
                cprint(colors.YELLOW, "Execution interrupted by user. Exiting Metatag.")
                break

        sys.exit(0)

    # 3. FALLBACK DEFAULT LOGIC
    # Since positional arguments are currently disabled in cli.py, running
    # the application without any flags would cause it to silently do nothing.
    # This block provides a helpful message guiding users to the interactive flag.
    cprint(
        colors.CYAN,
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
