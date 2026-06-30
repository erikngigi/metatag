"""Interactive Terminal Wizard and API Client.

Acts as an interactive view component that manages terminal user prompts,
gathers choices, and queries the TVMaze API to discover metadata.
"""

from __future__ import annotations

import subprocess
import sys
from typing import TYPE_CHECKING, Any

from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator

from metatag.models.schemas.anime import AnimeSearchQuery
from metatag.views.theme import Theme, custom_style

if TYPE_CHECKING:
    from metatag.models.schemas.anime import AnimeDetailsSchema, AnimeEpisodeResponse
    from metatag.models.schemas.tvmaze import TVSeasonSchema, TVShowSchema


class InteractiveWizard:
    """Manages the step-by-step console setup wizard."""

    def __init__(self) -> None:
        pass

    def prompt_media_type(self) -> str:
        """Select between TV Shows and Anime."""
        try:
            media_selection = inquirer.select(
                message="Select Media Type:",
                choices=[
                    {"name": "  Anime", "value": "anime_series"},
                    {"name": "  TV", "value": "tv_series"},
                    {"name": "  Exit", "value": "exit"},
                ],
                style=custom_style,
            ).execute()

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation Cancelled.{Theme.RESET}")
            sys.exit(0)

        if media_selection == "exit":
            print(f"{Theme.YELLOW}Exiting Metatag renamer.{Theme.RESET}")
            sys.exit(1)

        return str(media_selection)

    def prompt_show_name(self) -> str:
        """Get the TV Show name from the user via text prompt."""
        try:
            show_name = inquirer.text(
                message="Search TV Show:",
                style=custom_style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="TV Show name cannot be empty.",
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

        return str(show_name.strip())

    def prompt_show_selection(self, preformatted_choices: list[dict[str, Any]]) -> TVShowSchema:
        """Display pre-formatted show choices directly to the user."""
        try:
            selected_show: TVShowSchema = inquirer.select(
                message="Select Show:", choices=preformatted_choices, style=custom_style
            ).execute()

            return selected_show

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

    def prompt_season_selection(self, preformatted_choices: list[dict[str, Any]]) -> TVSeasonSchema:
        """Display pre-formatted season choices directly to the user."""
        try:
            selected_season: TVSeasonSchema = inquirer.select(
                message="Select Season:",
                choices=preformatted_choices,
                style=custom_style,
            ).execute()

            return selected_season

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

    def display_episode_manifest(self, episode_names: list[str]) -> None:
        """Prints the upcoming target filename layout to the terminal screen."""
        for name in episode_names:
            print(f"{Theme.BLUE}   {Theme.RESET}{name}")
        print()

    def prompt_metadata_checkpoint(self) -> str:
        """Prompts the user to continue to file renaming or exit after viewing the episodes list."""
        try:
            next_action = inquirer.select(
                message="Choose Next Action:",
                choices=[
                    {"name": "󰑕  Rename Files", "value": "rename"},
                    Separator("─" * 25),
                    {"name": "󱇒  Select Another Season", "value": "alternate_season"},
                    {"name": "󱇒  Search Another Title", "value": "search_again"},
                    Separator("─" * 25),
                    {"name": "󰩈  Exit Metatag", "value": "exit"},
                ],
                style=custom_style,
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

        if next_action == "exit":
            print(f"{Theme.GREY}Exiting. No files were modified.{Theme.RESET}")
            sys.exit(0)

        return str(next_action)

    def prompt_post_rename_options(self) -> str:
        """Prompts the user on what to do after a successful rename execution."""
        try:
            next_action = inquirer.select(
                message="Renaming Complete. What would you like to do next?",
                choices=[
                    {"name": "󰑕  Run Another Rename Cycle", "value": "search_again"},
                    Separator("─" * 25),
                    {"name": "󰿅  Exit Metatag", "value": "exit"},
                ],
                style=custom_style,
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

        return str(next_action)

    def prompt_target_directory(self, default_path: str) -> str:
        """Prompts the user to pick a source directory with live tab-completion."""
        try:
            target_dir = inquirer.filepath(
                message="Select Directory:",
                style=custom_style,
                default=default_path,
                only_directories=True,
                validate=PathValidator(is_dir=True, message="Target directory path does not exist."),
            ).execute()
            return str(target_dir)
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation Cancelled.{Theme.RESET}")
            sys.exit(1)

    def prompt_rename_type(self) -> str:
        """Select between renaming subtitles and video files."""
        try:
            rename_selection = inquirer.select(
                message="Select Filetype:",
                choices=[
                    {"name": " mkv/mp4", "value": "video"},
                    {"name": "󰨖 srt", "value": "subtitle"},
                ],
                style=custom_style,
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation Cancelled.{Theme.RESET}")
            sys.exit(0)

        return str(rename_selection)

    def prompt_confirmation(self, message: str, default: bool = True) -> bool:
        """A generic reusable confirmation prompt that returns a boolen choice."""
        try:
            return bool(inquirer.confirm(message=message, default=default, style=custom_style).execute())
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

    def prompt_rename_confirmation(self) -> bool:
        """Prompts the user to verify and confirm the file renaming actions."""
        try:
            rename_prompt = inquirer.confirm(
                message="Do you want to proceed with renaming these files?", default=False, style=custom_style
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

        return bool(rename_prompt)

    def prompt_anime_search_filters(self) -> AnimeSearchQuery:
        """Prompts for show name, format type, and airing status sequentially."""
        try:
            # 1. Input for Anime Name
            anime_name = inquirer.text(
                message="Enter Anime Name to search:",
                style=custom_style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="Search term cannot be empty.",
            ).execute()

            # 2. Select for Format Type
            anime_type = inquirer.select(
                message="Filter by Format Type:",
                choices=[
                    {"name": "📺 TV Show", "value": "tv"},
                    {"name": "🎬 Movie", "value": "movie"},
                    {"name": "💿 OVA / Special", "value": "ova"},
                    Separator(),
                    {"name": "🌐 Any Format", "value": ""},
                ],
                style=custom_style,
                mandatory=True,
            ).execute()

            # 3. Select for Airing Status
            anime_status = inquirer.select(
                message="Filter by Airing Status:",
                choices=[
                    {"name": "🏁 Finished Airing", "value": "complete"},
                    {"name": "📡 Currently Airing", "value": "airing"},
                    {"name": "📅 Upcoming", "value": "upcoming"},
                    Separator(),
                    {"name": "🌐 Any Status", "value": ""},
                ],
                style=custom_style,
                mandatory=True,
            ).execute()

            return AnimeSearchQuery(
                anime_name=anime_name.strip(),
                anime_type=anime_type,
                anime_status=anime_status,
            )

        except KeyboardInterrupt:
            print(f"{Theme.RED}\nOperation cancelled.{Theme.RESET}")
            sys.exit(1)

    def prompt_anime_selection(self, preformatted_choices: list[dict[str, Any]]) -> AnimeDetailsSchema:
        """Display pre-formatted show choices directly to the user."""
        try:
            total_anime_count = len(preformatted_choices)
            selected_anime: AnimeDetailsSchema = inquirer.select(
                message="Select Show:",
                choices=preformatted_choices,
                style=custom_style,
                instruction=f"[Use arrows to navigate, total: {total_anime_count} items]",
            ).execute()

            return selected_anime

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

    def prompt_anime_page_selection(self, max_pages: int) -> int:
        """Prompts the user to select an explicit page index when viewing multi-page lists.

        Args:
            max_pages: The maximum number of pages found in the metadata profile.

        Returns:
            The integer index of the selected page choice.
        """
        try:
            page_choices = [{"name": f"📄 Page {i} of {max_pages}", "value": i} for i in range(1, max_pages + 1)]

            # inquirer.select returns the 'value' key of the chosen dictionary item, which is an integer!
            selected_page: int = inquirer.select(
                message="Multiple episode pages found. Select a metadata chunk page to view:",
                choices=page_choices,
                default=1,
            ).execute()

            return selected_page

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

    def clear_screen(self) -> None:
        """Clears the Linux terminal screen securely using subprocess."""
        subprocess.run(["clear"])
