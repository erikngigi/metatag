"""Main API Selector Controller.

Orchestrates the media-type routing and delegates control to a specific
sub-controllers based on the user's selection criteria.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.controllers.tv_selector import TVSelectorController
from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.interactive import InteractiveWizard


class APISelectorController:
    """Main entry point for API metadata selection routing."""

    def __init__(self, wizard: InteractiveWizard, tvmaze: TVMazeModel) -> None:
        self.wizard = wizard
        self.tvmaze = tvmaze

    def run(self) -> tuple[str, int, list[Any]]:
        """Determines media type and delegates execution to sub-controllers."""
        while True:
            print(f"{Theme.GREY}To cancel this prompt press ctrl+c{Theme.RESET}")

            # Step 1: Prompt for media type ("tv_series" or "anime")
            media_type = self.wizard.prompt_media_type()

            if media_type == "tv_series":
                tv_controller = TVSelectorController(self.wizard, self.tvmaze)
                return tv_controller.execute()

            elif media_type == "anime":
                print(f"{Theme.YELLOW}Anime integration is coming soon.{Theme.RESET}")
                print(f"{Theme.CYAN}Restarting Metatag Wizard.{Theme.RESET}")
                self.wizard.clear_screen()
                continue
