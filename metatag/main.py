"""Application Bootstrapper and Router.

Acts as the root orchestrator of the metatag application. Parses terminal
flags and conditionally hands off execution to the appropriate controller layer.
"""

from __future__ import annotations

import sys

from metatag.cli import CLIArgs, parse_arguments
from metatag.colors import colors, cprint
from metatag.controllers.workflow_router import WorkflowRouterController
from metatag.models.anime_model import AnimeTenraiModel
from metatag.models.tvmaze_model import TVMazeModel
from metatag.views.anime_menu import AnimeMenuView
from metatag.views.base_menu import BaseMenuView
from metatag.views.tv_menu import TVMenuView


def run_interactive_wizard(cli_args: CLIArgs) -> None:
    """Orchestrates the interactive wizard lifecycle."""
    # 1. Instantiate Data Engine (Models) & UI (Views)
    anime_tenrai = AnimeTenraiModel()
    tvmaze = TVMazeModel()
    base_menu = BaseMenuView()
    anime_menu = AnimeMenuView()
    tvmenu = TVMenuView()

    # 2. Inject dependencies into Controller once
    workflow_controller = WorkflowRouterController(
        base_menu=base_menu,
        anime_tenrai=anime_tenrai,
        anime_menu=anime_menu,
        tvmaze=tvmaze,
        tvmenu=tvmenu,
    )

    # 3. Interactive Execution Loop
    while True:
        try:
            workflow_controller.dispatch(cli_args)

            next_move = base_menu.prompt_post_rename_options()
            if next_move == "exit":
                cprint(colors.YELLOW, "Exiting Metatag. Goodbye.")
                break

            base_menu.clear_screen()

        except KeyboardInterrupt:
            cprint(colors.YELLOW, "\nExecution interrupted by user. Exiting Metatag.")
            break

    sys.exit(0)


def main() -> None:
    """Orchestrates system startup and conditional flag routing."""
    cli_args = parse_arguments()

    # if cli_args.interactive:
    #     run_interactive_wizard(cli_args)
    if cli_args.interactive:
        run_interactive_wizard(cli_args)

    # Fallback message if run without flags
    cprint(
        colors.CYAN,
        "Welcome to metatag!\nPlease launch the interactive metadata explorer using:\n\n    $ metatag --interactive\n",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
