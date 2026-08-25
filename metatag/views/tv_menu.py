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
                message="Enter TV series name to search:",
                style=self.show_name_style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="TV show name cannot be empty.",
            ).execute()
        )
        return show_name.strip()

    def prompt_show_selection(self, show_choices: list[dict[str, Any]]) -> TVShowSchema:
        """Display pre-formatted show choices directly to the user."""
        selected_show: TVShowSchema = self._safe_prompt(
            lambda: inquirer.select(
                message="Select matching TV series:", choices=show_choices, style=self.show_selection_style
            ).execute()
        )

        return selected_show

    def prompt_season_selection(self, season_choices: list[dict[str, Any]]) -> TVSeasonSchema:
        """Display pre-formatted season choices directly to the user."""
        selected_seasons: TVSeasonSchema = self._safe_prompt(
            lambda: inquirer.select(
                message="Select season to map:", choices=season_choices, style=self.season_selection_style
            ).execute()
        )

        return selected_seasons

    def prompt_tv_checkpoint(self) -> str:
        """Prompts the user for their next action after displayinh the TV season episodes.

        Allows the user to proceed with file renaming, revert to selecting an alternate
        season for the current show, search for a different title, or exit.
        """
        next_action: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Select next step:",
                choices=[
                    {"name": "Proceed to File Selection & Renaming", "value": "rename"},
                    {"name": "Preview Episodes for"},
                    {"name": "Select a Different Season", "value": "alternate_season"},
                    {"name": "Search for Another TV Series", "value": "search_again"},
                    {"name": "Exit Metatag", "value": "exit"},
                ],
                instruction="(Use  arrows to navigate)",
                style=self.checkpoint_style,
            ).execute(),
            exit_code=0,
        )

        if next_action == "exit":
            cprint(colors.RED, "Operation cancelled.")
            sys.exit(0)

        return next_action
