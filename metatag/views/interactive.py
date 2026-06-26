"""Interactive Terminal Wizard and API Client.

Acts as an interactive view component that manages terminal user prompts,
gathers choices, and queries the TVMaze API to discover metadata.
"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import Any

import requests
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from metatag.views.theme import Theme, custom_style


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
                    {"name": "Anime Servies", "value": "anime_series"},
                    {"name": "Tv Series", "value": "tv_series"},
                ],
                style=custom_style,
            ).execute()

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation Cancelled.{Theme.RESET}")
            sys.exit(0)

        if media_selection == "anime_series":
            print(f"{Theme.YELLOW}Anime support is currently under development.{Theme.RESET}")
            sys.exit(1)

        return str(media_selection)

    def prompt_show_name(self) -> str:
        """Get the TV Show name from the user via text prompt."""
        try:
            show_name = inquirer.text(
                message="Search for Tv Show using TVMaze API:",
                style=custom_style,
                validate=lambda text: len(text.strip()) > 0,
                invalid_message="TV Show name cannot be empty.",
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

        return str(show_name.strip())

    def prompt_show_selection(self, preformatted_choices: list[dict[str, Any]]) -> dict[str, Any]:
        """Display pre-formatted show choices directly to the user."""
        try:
            selected_show: dict[str, Any] = inquirer.select(
                message="Select a show from the search list:", choices=preformatted_choices, style=custom_style
            ).execute()

            return selected_show

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
            sys.exit(0)

    def prompt_season_selection(self, preformatted_choices: list[dict[str, Any]]) -> dict[str, Any]:
        """Display pre-formatted season choices directly to the user."""
        try:
            selected_season: dict[str, Any] = inquirer.select(
                message="Select a season to inspect the episode list:",
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
            print(f"{Theme.GREEN}->{Theme.RESET} {name}")
        print()

    def prompt_continue_or_exit(self) -> str:
        """Prompts the user to continue to file renaming or exit after viewing the episodes list."""
        try:
            next_action = inquirer.select(
                message="Choose your next action:",
                choices=[
                    {"name": "Rename Tv Show files", "value": "continue"},
                    {"name": "Restart Metatag", "value": "restart"},
                    {"name": "Exit Metatag", "value": "exit"},
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

    def prompt_target_directory(self, default_path: str) -> str:
        """Prompts the user to pick a source directory with live tab-completion."""
        try:
            target_dir = inquirer.filepath(
                message="Select source target directory:",
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
                message="Select File Type:",
                choices=[
                    {"name": "video files (mkv or mp4)", "value": "video"},
                    {"name": "subtitle files (srt)", "value": "subtitle"},
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

    def clear_screen(self) -> None:
        """Clears the Linux terminal screen securely using subprocess."""
        subprocess.run(["clear"])
