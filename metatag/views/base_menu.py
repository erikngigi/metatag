"""Base configuration and shared components for the InquirerPy CLI menus.

This module houses the central style definitions, shared validation logic,
and common navigation options (such as 'Back' and 'Exit' utilities) utilized
by both the TV Show and Anime menu modules. It ensures a consistent UI/UX
across all interactive terminal prompts.
"""

import subprocess
import sys
from typing import Any, Callable

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from metatag.colors import colors, cprint, custom_style


class BaseMenuView:
    """Renders common CLI components like styles, headers, and exit prompts."""

    def __init__(self) -> None:
        self.style = custom_style

    def _safe_prompt(self, prompt_func: Callable[[], Any], exit_code: int = 0) -> Any:
        """Helper wrapper to handle KeyboardInterrupt globally across menus."""
        try:
            return prompt_func()
        except KeyboardInterrupt:
            cprint(colors.YELLOW, "Operation cancelled.")
            sys.exit(exit_code)

    def clear_screen(self) -> None:
        """Clears the Linux terminal screen securely using subprocess."""
        subprocess.run(["clear"])

    def prompt_media_type(self) -> str:
        """Select between TV Show and Anime."""
        media_selection = self._safe_prompt(
            lambda: inquirer.select(
                message="Select Media Type:",
                choices=[
                    {"name": "1. Anime (Jikan API)", "value": "anime_series"},
                    {"name": "2. TV (TVMaze API)", "value": "tv_series"},
                    {"name": "3. Exit Metatag", "value": "exit"},
                ],
                long_instruction="To cancel this prompt press, ctrl+c",
                style=self.style,
            ).execute(),
            exit_code=0,
        )

        if media_selection == "exit":
            cprint(colors.YELLOW, "Exiting Metatag Renamer.")
            sys.exit(1)

        return str(media_selection)

    def prompt_target_directory(self, default_path: str) -> str:
        """Prompts the user to pick a source directory with live tab-completions."""
        return str(
            self._safe_prompt(
                lambda: inquirer.filepath(
                    message="Select Directory:",
                    style=self.style,
                    default=default_path,
                    only_directories=True,
                    validate=PathValidator(is_dir=True, message="Target directory path does not exist."),
                ).execute(),
                exit_code=1,
            )
        )

    def prompt_filetype_rename(self) -> str:
        """Select filetype you want to rename (e.g., subtitles, videos)"""
        rename_filetype_selection: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Select filetype to rename:",
                choices=[
                    {"name": "mkv/mp4", "value": "video"},
                    {"name": "srt", "value": "subtitle"},
                ],
                long_instruction="To cancel this prompt press, ctrl+c",
                style=self.style,
            ).execute()
        )

        return rename_filetype_selection

    def prompt_confirmation(self, message: str, default: bool) -> bool:
        """A generic reusable confirmation prompt that returns a boolen choice."""
        return bool(self._safe_prompt(lambda: inquirer.confirm(message=message, default=default, style=self.style)))

    def print_episodes(self, episode_list: list[str]) -> None:
        """Prints the pre-formatted episode names of the selected media type."""
        for name in episode_list:
            cprint(colors.WHITE, f"{name}")
        print()

    def prompt_post_rename_options(self) -> str:
        """Prompts the user on next actions after succesful renaming process."""
        post_rename_action: str = self._safe_prompt(
            lambda: inquirer.select(
                message="Renaming process complete. Choose next action?",
                choices=[
                    {"name": "Run Another Rename Cycle", "value": "search_again"},
                    {"name": "Exit Metatag", "value": "exit"},
                ],
                style=self.style,
            ).execute()
        )

        return post_rename_action
