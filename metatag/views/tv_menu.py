"""Interactive terminal views for television media renaming workflows.

This module leverages InquirerPy to guide the user through selecting,
filtering, and mapping TV show files. It extends `BaseMenuView` to provide
specific prompts for processing standard seasonal television formats.
"""

import sys
from typing import TYPE_CHECKING, Any

from InquirerPy import inquirer

from metatag.colors import colors, cprint
from metatag.views.base_menu import BaseMenuView

if TYPE_CHECKING:
    from metatag.models.schemas.tvmaze import TVSeasonSchema, TVShowSchema


class TVMenuView(BaseMenuView):
    """Inherits base styles and renders TV-Specific selection menus."""

    def prompt_show_name(self) -> str:
        """Get the TV show name from the user via text prompt."""
        show_name: str = self._safe_prompt(
            lambda: inquirer.text(
                message="Search TV Show:",
                style=self.style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="TV show name cannot be empty.",
            ).execute()
        )
        return show_name.strip()

    def prompt_show_selection(self, show_choices: list[dict[str, Any]]) -> TVShowSchema:
        """Display pre-formatted show choices directly to the user."""
        selected_show: TVShowSchema = self._safe_prompt(
            lambda: inquirer.select(message="Select Show:", choices=show_choices, style=self.style).execute()
        )

        return selected_show

    def prompt_season_selection(self, season_choices: list[dict[str, Any]]) -> TVSeasonSchema:
        """Display pre-formatted season choices directly to the user."""
        selected_seasons: TVSeasonSchema = self._safe_prompt(
            lambda: inquirer.select(message="Selected Season:", choices=season_choices, style=self.style).execute()
        )

        return selected_seasons

    def prompt_tv_checkpoint(self) -> str:
        """Prompts the user for their next action after displayinh the TV season episodes.

        Allows the user to proceed with file renaming, revert to selecting an alternate
        season for the current show, search for a different title, or exit.
        """
        next_action: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Choose next action:",
                choices=[
                    {"name": "Rename tv files", "value": "rename"},
                    {"name": "Select alternate season", "value": "alternate_season"},
                    {"name": "Search alternate tv show", "value": "search_again"},
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
