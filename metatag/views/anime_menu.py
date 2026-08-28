"""Interactive terminal views for anime media renaming workflows.

This module leverages InquirerPy to manage user interactions tailored specifically
to anime libraries. It extends `BaseMenuView` to handle absolute episode
number formats, pagination, and specialized search filters.
"""

import sys
from typing import TYPE_CHECKING, Any

from InquirerPy import inquirer

from metatag.colors import colors, cprint
from metatag.models.schemas.anime import AnimeSearchQuery
from metatag.views.base_menu import BaseMenuView

if TYPE_CHECKING:
    from metatag.models.schemas.anime import AnimeDetailsSchema


class AnimeMenuView(BaseMenuView):
    """Inherits base styles and renders anime-specific filter and search components."""

    def prompt_anime_search_filters(self) -> AnimeSearchQuery:
        """Prompts for anime name, format type, and airing status sequentially."""

        anime_name: str = self._safe_prompt(
            lambda: inquirer.text(
                instruction="(Ctrl+C to cancel)",
                message="Enter anime name to search:",
                style=self.show_title_style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="Search term cannot be empty.",
            ).execute(),
            exit_code=1,
        )

        anime_type: str = self._safe_prompt(
            lambda: inquirer.select(
                instruction="(Use arrow keys to navigate and Enter to select)",
                long_instruction="To cancel this prompt press Ctrl+C",
                message="Filter by Format Type:",
                choices=[
                    {"name": "All Formats (No filter applied)", "value": None},
                    {"name": "TV Series (Seasonal broadcast & episodic shows)", "value": "tv"},
                    {"name": "Feature Movie (Theatrical & full-length films)", "value": "movie"},
                    {"name": "OVA / Special (Original video animations & side stories)", "value": "ova"},
                ],
                style=self.show_selection_style,
                mandatory=True,
            ).execute(),
            exit_code=1,
        )

        anime_status: str = self._safe_prompt(
            lambda: inquirer.select(
                instruction="(Use arrow keys to navigate and Enter to select)",
                long_instruction="To cancel this prompt press Ctrl+C",
                message="Filter by Airing Status:",
                choices=[
                    {"name": "All Statuses (No filter applied)", "value": None},
                    {"name": "Finished Airing (Completed broadcasts & released media)", "value": "complete"},
                    {"name": "Currently Airing (Active seasonal broadcasts)", "value": "airing"},
                    {"name": "Upcoming (Unreleased & announced series)", "value": "upcoming"},
                ],
                style=self.show_selection_style,
                mandatory=True,
            ).execute(),
            exit_code=1,
        )

        return AnimeSearchQuery(
            anime_name=anime_name.strip(),
            anime_type=anime_type,
            anime_status=anime_status,
        )

    def prompt_anime_selection(self, anime_choices: list[dict[str, Any]]) -> AnimeDetailsSchema:
        """Display a pre-formatted anime choices list."""
        anime_selected: AnimeDetailsSchema = self._safe_prompt(
            lambda: inquirer.select(
                instruction="(Use arrow keys to navigate and Enter to select)",
                long_instruction="To cancel this prompt press Ctrl+C",
                message="Select Show:",
                choices=anime_choices,
                style=self.show_selection_style,
            ).execute()
        )

        return anime_selected

    def prompt_anime_page_selection(self, max_pages: int) -> int:
        """Prompts the user to select an explicit page index when viewing multi-page lists."""

        page_choices = [{"name": f"Page {i} of {max_pages}", "value": i} for i in range(1, max_pages + 1)]

        selected_page: int = self._safe_prompt(
            lambda: inquirer.select(
                instruction="(Use arrow keys to navigate and Enter to select)",
                long_instruction="To cancel this prompt press Ctrl+C",
                message="Multiple episode pages found. Select a metadata chunk page to view:",
                choices=page_choices,
                default=1,
                style=self.show_selection_style,
            ).execute()
        )

        return selected_page

    def print_anime_episode_manifest(
        self,
        show_name: str,
        episode_list: list[str],
    ) -> None:
        """Prints an episode manifest framed with top header and bottom footer rules."""

        cprint(colors.BLUE_BOLD_UNDERLINE, f"\n{show_name}\n")

        # Episode Items (Clean, left-aligned without side padding or side borders)
        for name in episode_list:
            cprint(colors.BLUE_BOLD, f"  {name}")

    def prompt_anime_post_checkpoint(self) -> str:
        """Prompts the user for their next action after displaying the Anime episode manifest.

        Allows the user to proceed with file renaming, revert to selecting an alternate
        episode page for the current anime, search for a different title, or exit.
        """
        next_action: str = self._safe_prompt(
            lambda: inquirer.select(
                instruction="(Use arrow keys to navigate and Enter to select)",
                long_instruction="To cancel this prompt press Ctrl+C",
                message="Choose next action:",
                choices=[
                    {"name": "Proceed to File Selection & Renaming", "value": "rename"},
                    {"name": "Select a Different Episode Page", "value": "alternate_page"},
                    {"name": "Search for Another Anime Series", "value": "search_again"},
                    {"name": "Exit Metatag", "value": "exit"},
                ],
                style=self.post_manifest_action_style,
            ).execute(),
            exit_code=0,
        )

        if next_action == "exit":
            cprint(colors.YELLOW_BOLD, "Exited Metatag")
            sys.exit(0)

        return next_action
