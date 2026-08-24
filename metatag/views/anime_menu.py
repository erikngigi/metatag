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
                message="Enter anime name to search:",
                style=self.style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="Search term cannot be empty.",
            ).execute(),
            exit_code=1,
        )

        anime_type: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Filter by Format Type:",
                choices=[
                    {"name": "Any format", "value": None},
                    {"name": "Movie", "value": "movie"},
                    {"name": "OVA/Special", "value": "ova"},
                    {"name": "TV Show", "value": "tv"},
                ],
                style=self.style,
                mandatory=True,
            ).execute(),
            exit_code=1,
        )

        anime_status: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Filter by Airing Status:",
                choices=[
                    {"name": "Any Status", "value": None},
                    {"name": "Currently Airing", "value": "airing"},
                    {"name": "Finished Airing", "value": "complete"},
                    {"name": "Upcoming", "value": "upcoming"},
                ],
                style=self.style,
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
        anime_count = len(anime_choices)
        anime_selected: AnimeDetailsSchema = self._safe_prompt(
            lambda: inquirer.select(
                message="Select Show:",
                choices=anime_choices,
                style=self.style,
                instruction=f"[Use arrows to navigate] Items: {anime_count}/{anime_count}",
                long_instruction="To cancel this prompt press, ctrl+c",
            ).execute()
        )

        return anime_selected

    def prompt_anime_page_selection(self, max_pages: int) -> int:
        """Prompts the user to select an explicit page index when viewing multi-page lists."""

        page_choices = [{"name": f"Page {i} of {max_pages}", "value": i} for i in range(1, max_pages + 1)]

        selected_page: int = self._safe_prompt(
            lambda: inquirer.select(
                message="Multiple episode pages found. Select a metadata chunk page to view:",
                choices=page_choices,
                default=1,
                style=self.style,
            ).execute()
        )

        return selected_page

    def prompt_anime_checkpoint(self) -> str:
        """Prompts the user for their next action after displaying the Anime episode manifest.

        Allows the user to proceed with file renaming, revert to selecting an alternate
        episode page for the current anime, search for a different title, or exit.
        """
        next_action: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Choose next action:",
                choices=[
                    {"name": "Rename anime files", "value": "rename"},
                    {"name": "Select alternate page", "value": "alternate_page"},
                    {"name": "Search alternate anime", "value": "search_again"},
                    {"name": "Exit", "value": "exit"},
                ],
                style=self.style,
            ).execute(),
            exit_code=0,
        )

        if next_action == "exit":
            cprint(colors.RED, "Operation cancelled.")
            sys.exit(1)

        return next_action
