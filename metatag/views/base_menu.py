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
    colors,
    confirm_prompt_style,
    cprint,
    directory_selection_style,
    filetype_selection_style,
    media_selection_style,
    post_manifest_action_style,
    post_rename_style,
    show_selection_style,
    show_title_style,
)


class BaseMenuView:
    """Renders common CLI components like styles, headers, and exit prompts."""

    def __init__(self) -> None:
        self.media_selection_style = media_selection_style
        self.show_title_style = show_title_style
        self.show_selection_style = show_selection_style
        self.directory_selection_style = directory_selection_style
        self.filetype_selection_style = filetype_selection_style
        self.checkbox_selection_style = checkbox_selection_style
        self.confirm_prompt_style = confirm_prompt_style
        self.post_rename_style = post_rename_style
        self.post_manifest_action_style = post_manifest_action_style

    def _safe_prompt(self, prompt_func: Callable[[], Any], exit_code: int = 0) -> Any:
        """Helper wrapper to handle KeyboardInterrupt globally across menus."""
        try:
            return prompt_func()
        except KeyboardInterrupt:
            cprint(colors.YELLOW_BOLD, "Exited Metatag")
            sys.exit(exit_code)

    def clear_screen(self) -> None:
        """Clears the Linux terminal screen securely using subprocess."""
        subprocess.run(["clear"])

    def prompt_main_menu(self) -> str:
        """Prompts for the primary action track: media renaming, universal metadata editing, or exit."""
        main_menu = self._safe_prompt(
            lambda: inquirer.select(
                pointer="",
                instruction="Use arrow keys to navigate and Enter to select.",
                long_instruction="To cancel this prompt press ctrl+c",
                message="Select action track to process:",
                choices=[
                    {"name": "Rename Anime Series", "value": "anime_series"},
                    {"name": "Rename TV Show Series", "value": "tv_series"},
                    {"name": "Edit Embedded File Metadata (MKV / MP4)", "value": "metadata_edit"},
                    {"name": "Exit", "value": "exit"},
                ],
                style=self.media_selection_style,
            ).execute(),
            exit_code=0,
        )

        if main_menu == "exit":
            cprint(colors.YELLOW, "Exited Metatag")
            sys.exit(0)

        return str(main_menu)

    def prompt_target_directory(self, choices: list[str]) -> str:
        """Prompts the user to pick a target directory from a pre-scanned list."""
        return str(
            self._safe_prompt(
                lambda: inquirer.fuzzy(
                    pointer="",
                    instruction="Use arrow keys to navigate and Enter to select.",
                    long_instruction="To cancel this prompt press ctrl+c",
                    message="Select the target directory:",
                    choices=choices,
                    style=self.directory_selection_style,
                    match_exact=False,
                ).execute(),
                exit_code=1,
            )
        )

    def prompt_filetype_rename(self) -> str:
        """Select filetype you want to rename (e.g., subtitles, videos)"""
        rename_filetype_selection: str = self._safe_prompt(
            lambda: inquirer.select(
                pointer="",
                instruction="Use arrow keys to navigate and Enter to select.",
                long_instruction="To cancel this prompt press ctrl+c",
                message="Filter target file extension(s):",
                choices=[
                    {"name": "Video Files (.mkv, .mp4)", "value": "video"},
                    {"name": "Subtitle Files (.srt)", "value": "subtitle"},
                ],
                style=self.filetype_selection_style,
            ).execute()
        )

        return rename_filetype_selection

    def prompt_episode_selection(self, episode_manifest: list[str]) -> list[str]:
        """Prompts the user to multi-select which remote episodes match their local files."""
        episode_manifest_selection: list[str] = self._safe_prompt(
            lambda: inquirer.checkbox(
                pointer="",
                instruction="Use arrow keys to navigate, Space to toggle and Enter to select.",
                long_instruction="To cancel this prompt press ctrl+c",
                message="Select the episodes you want to match (Space to toggle, Enter to confirm)",
                enabled_symbol="󰋘 ",
                disabled_symbol="󰋙 ",
                choices=[{"name": ep, "value": ep, "enabled": True} for ep in episode_manifest],
                transformer=lambda result: "",
                style=self.checkbox_selection_style,
            ).execute(),
            exit_code=0,
        )

        return episode_manifest_selection

    def prompt_confirmation(self, message: str, default: bool) -> bool:
        """A generic reusable confirmation prompt that returns a boolen choice."""
        prompt_confirm: bool = self._safe_prompt(
            lambda: inquirer.confirm(
                instruction="(y/N, Ctrl+C to cancel)",
                message=message,
                default=default,
                confirm_letter="y",
                reject_letter="N",
                style=self.confirm_prompt_style,
            ).execute()
        )

        return prompt_confirm

    def prompt_post_rename_options(self) -> str:
        """Prompts the user on next actions after succesful renaming process."""
        post_rename_action: str = self._safe_prompt(
            lambda: inquirer.select(
                instruction="Use arrow keys to navigate and Enter to select.",
                long_instruction="To cancel this prompt press ctrl+c",
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
                instruction="Use arrow keys to navigate and Enter to select.",
                long_instruction="To cancel this prompt press ctrl+c",
                message="Select the local files you want to rename (Space to toggle, Enter to confirm)",
                enabled_symbol="󰋘",
                disabled_symbol="󰋙",
                choices=[{"name": f, "value": f, "enabled": True} for f in local_files],
                transformer=lambda result: f"  Selected files: [{len(result)}]",
                style=self.checkbox_selection_style,
            ).execute(),
            exit_code=0,
        )

        return local_file_selection
