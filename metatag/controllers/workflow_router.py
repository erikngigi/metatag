"""Main API Selector Controller.

Orchestrates media-type routing and delegates control to explicit setup
methods for individual media sub-controllers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.colors import colors, cprint
from metatag.controllers.anime.workflow import AnimeSelectorController
from metatag.controllers.shared.metadata_editor import MetadataController
from metatag.controllers.tv.workflow import TVSelectorController

if TYPE_CHECKING:
    from metatag.models.anime_model import AnimeTenraiModel
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.anime_menu import AnimeMenuView
    from metatag.views.base_menu import BaseMenuView
    from metatag.views.tv_menu import TVMenuView


class WorkflowRouterController:
    """Main entry point for routing user media choices to individual sub-controllers."""

    def __init__(
        self,
        anime_tenrai: AnimeTenraiModel,
        anime_menu: AnimeMenuView,
        base_menu: BaseMenuView,
        tvmaze: TVMazeModel,
        tvmenu: TVMenuView,
    ) -> None:
        self.tenrai = anime_tenrai
        self.anime_menu = anime_menu
        self.base_menu = base_menu
        self.tvmaze = tvmaze
        self.tvmenu = tvmenu

    def dispatch(self, cli_args: Any) -> None:
        """Prompts for media type and dispatches control to the target workflow."""
        main_menu_selection = self.base_menu.prompt_main_menu()

        if main_menu_selection == "tv_series":
            self.dispatch_tv_workflow(cli_args)
        elif main_menu_selection == "anime_series":
            self.dispatch_anime_workflow(cli_args)
        elif main_menu_selection == "metadata_edit":
            self.dispatch_metadata_workflow()
        elif main_menu_selection == "exit":
            cprint(colors.YELLOW, "Exiting menu routing track...")

    def dispatch_tv_workflow(self, cli_args: Any) -> None:
        """Explicitly handles the initialization and execution lifecycle of TV Series."""
        tv_controller = TVSelectorController(self.base_menu, self.tvmaze, self.tvmenu)
        tv_controller.execute(cli_args)

    def dispatch_anime_workflow(self, cli_args: Any) -> None:
        """Explicitly handles the initialization and execution lifecycle of Anime Series."""
        anime_controller = AnimeSelectorController(self.anime_menu, self.base_menu, self.tenrai)
        anime_controller.execute(cli_args)

    def dispatch_metadata_workflow(self) -> None:
        """Explicitly handles updating embedded MKV title metadata."""
        metadata_controller = MetadataController(self.base_menu)
        metadata_controller.run()
