"""Main API Selector Controller.

Orchestrates media-type routing and delegates control to explicit setup
methods for individual media sub-controllers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.colors import colors, cprint
from metatag.controllers.anime.workflow import AnimeSelectorController
from metatag.controllers.tv.workflow import TVSelectorController

if TYPE_CHECKING:
    from metatag.models.anime_model import AnimeTenraiModel
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.anime_menu import AnimeMenuView
    from metatag.views.base_menu import BaseMenuView
    from metatag.views.tv_menu import TVMenuView


class APISelectorController:
    """Main entry point for routing and setting up API metadata selections."""

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

    def run(self, cli_args: Any) -> None:
        """High-level orchestrator that determines media routing tracks."""
        # Prompt for media type ("tv_series", "anime_series", or "exit")
        media_type = self.base_menu.prompt_media_type()

        if media_type == "tv_series":
            self._handle_tv_routing(cli_args)
        elif media_type == "anime_series":
            self._handle_anime_routing(cli_args)
        elif media_type == "exit":
            cprint(colors.YELLOW, "Exiting menu routing track...")

    def _handle_tv_routing(self, cli_args: Any) -> None:
        """Explicitly handles the initialization and execution lifecycle of TV Series."""
        tv_controller = TVSelectorController(self.base_menu, self.tvmaze, self.tvmenu)
        tv_controller.execute(cli_args)

    def _handle_anime_routing(self, cli_args: Any) -> None:
        """Explicitly handles the initialization and execution lifecycle of Anime Series."""
        anime_controller = AnimeSelectorController(self.anime_menu, self.base_menu, self.tenrai)
        anime_controller.execute(cli_args)
