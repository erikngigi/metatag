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
                style=self.show_title_style,
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
                message="Select season to map:", choices=season_choices, style=self.show_selection_style
            ).execute()
        )

        return selected_seasons

    def prompt_tv_post_manifest_action(self) -> str:
        """Prompts for the next step following the display of a TV show's episode manifest.

        Presents a menu for the user to proceed with target file selection and renaming,
        navigate back to choose another season within the same series, initiate a fresh
        TV series search, or safely terminate execution.

        Returns:
            str: The selected navigation token ('rename', 'alternate_season', 'search_again').
        """
        next_action: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Select next step:",
                choices=[
                    {"name": "Proceed to File Selection & Renaming", "value": "rename"},
                    {"name": "Select a Different Season", "value": "alternate_season"},
                    {"name": "Search for Another TV Series", "value": "search_again"},
                    {"name": "Exit Metatag", "value": "exit"},
                ],
                instruction="(Use ↑/↓ arrows to navigate)",
                style=self.post_manifest_action_style,
            ).execute(),
            exit_code=0,
        )

        if next_action == "exit":
            cprint(colors.YELLOW_BOLD, "Exited Metatag")
            sys.exit(0)

        return next_action
