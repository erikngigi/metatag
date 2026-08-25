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

from metatag.colors import (
    checkbox_selection_style,
    checkpoint_style,
    colors,
    confirmation_style,
    cprint,
    directory_selection_style,
    filetype_selection_style,
    media_selection_style,
    post_rename_style,
    season_selection_style,
    show_name_style,
    show_selection_style,
)


class BaseMenuView:
    """Renders common CLI components like styles, headers, and exit prompts."""

    def __init__(self) -> None:
        self.media_selection_style = media_selection_style
        self.show_name_style = show_name_style
        self.show_selection_style = show_selection_style
        self.season_selection_style = season_selection_style
        self.checkpoint_style = checkpoint_style
        self.directory_selection_style = directory_selection_style
        self.filetype_selection_style = filetype_selection_style
        self.checkbox_selection_style = checkbox_selection_style
        self.confirmation_style = confirmation_style
        self.post_rename_style = post_rename_style

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
                message="Select the media type to process:",
                choices=[
                    {"name": "Anime", "value": "anime_series"},
                    {"name": "TV Series", "value": "tv_series"},
                    {"name": "Exit", "value": "exit"},
                ],
                instruction="(Use  arrows to navigate)",
                long_instruction="To cancel this prompt press ctrl+c",
                style=self.media_selection_style,
            ).execute(),
            exit_code=0,
        )

        if media_selection == "exit":
            cprint(colors.YELLOW, "Exited Metatag")
            sys.exit(0)

        return str(media_selection)

    def prompt_target_directory(self, default_path: str) -> str:
        """Prompts the user to pick a source directory with live tab-completions."""
        return str(
            self._safe_prompt(
                lambda: inquirer.filepath(
                    message="Enter target folder path:",
                    style=self.directory_selection_style,
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
                message="Filter target file extension(s):",
                choices=[
                    {"name": "mkv/mp4", "value": "video"},
                    {"name": "srt", "value": "subtitle"},
                ],
                long_instruction="To cancel this prompt press, ctrl+c",
                style=self.filetype_selection_style,
            ).execute()
        )

        return rename_filetype_selection

    def prompt_episode_selection(self, episode_manifest: list[str]) -> list[str]:
        """Prompts the user to multi-select which remote episodes match their local files."""
        episode_manifest_selection: list[str] = self._safe_prompt(
            lambda: inquirer.checkbox(
                message="Select the episodes you want to match (Space to toggle, Enter to confirm)",
                choices=[{"name": ep, "value": ep, "enabled": True} for ep in episode_manifest],
                instruction="[Space] Toggle, [Enter] Confirm",
                transformer=lambda result: "",
                style=self.checkbox_selection_style,
            ).execute(),
            exit_code=0,
        )

        return episode_manifest_selection

    def prompt_confirmation(self, message: str, default: bool) -> bool:
        """A generic reusable confirmation prompt that returns a boolen choice."""
        return bool(
            self._safe_prompt(
                lambda: inquirer.confirm(message=message, default=default, style=self.confirmation_style).execute()
            )
        )

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
                style=self.post_rename_style,
            ).execute()
        )

        return post_rename_action

    def prompt_local_file_selection(self, local_files: list[str]) -> list[str]:
        """Prompts the user to multi-select which local files they want to include for renaming."""
        local_file_selection: list[str] = self._safe_prompt(
            lambda: inquirer.checkbox(
                message="Select the local files you want to rename (Space to toggle, Enter to confirm)",
                choices=[{"name": f, "value": f, "enabled": True} for f in local_files],
                instruction="[Space] Toggle, [Enter] Confirm",
                transformer=lambda result: f"{len(result)} file(s) selected",
                style=self.post_rename_style,
            ).execute(),
            exit_code=0,
        )

        return local_file_selection
