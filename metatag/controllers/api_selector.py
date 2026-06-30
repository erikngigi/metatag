"""Main API Selector Controller.

Orchestrates media-type routing and delegates control to explicit setup
methods for individual media sub-controllers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.controllers.anime_selector import AnimeSelectorController
from metatag.controllers.tv_selector import TVSelectorController
from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.models.anime_model import AnimeJikanModel
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.interactive import InteractiveWizard


class APISelectorController:
    """Main entry point for routing and setting up API metadata selections."""

    def __init__(self, wizard: InteractiveWizard, anime: AnimeJikanModel, tvmaze: TVMazeModel) -> None:
        self.wizard = wizard
        self.tvmaze = tvmaze
        self.anime = anime

    def run(self, args: Any) -> None:
        """High-level orchestrator that determines media routing tracks."""
        print(f"{Theme.GREY}To cancel this prompt press ctrl+c{Theme.RESET}")

        # Prompt for media type ("tv_series", "anime_series", or "exit")
        media_type = self.wizard.prompt_media_type()

        if media_type == "tv_series":
            self._handle_tv_routing(args)
        elif media_type == "anime_series":
            self._handle_anime_routing(args)
        elif media_type == "exit":
            print(f"{Theme.GREY}Exiting menu routing track...{Theme.RESET}")

    def _handle_tv_routing(self, args: Any) -> None:
        """Explicitly handles the initialization and execution lifecycle of TV Series."""
        print(f"{Theme.CYAN}Initializing TV Exploration Track...{Theme.RESET}")
        tv_controller = TVSelectorController(self.wizard, self.tvmaze)
        tv_controller.execute(args)

    def _handle_anime_routing(self, args: Any) -> None:
        """Explicitly handles the initialization and execution lifecycle of Anime Series."""
        print(f"{Theme.CYAN}Initializing Anime Exploration Track...{Theme.RESET}")
        anime_controller = AnimeSelectorController(self.wizard, self.anime)
        anime_controller.execute(args)
