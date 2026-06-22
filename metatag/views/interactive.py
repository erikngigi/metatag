"""Interactive Terminal Wizard and API Client.

Acts as an interactive view component that manages terminal user prompts,
gathers choices, and queries the TVMaze API to discover metadata.
"""

from __future__ import annotations

import sys
from typing import Any

import requests
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from metatag.views.theme import Theme, custom_style


class InteractiveWizard:
    """Manages the step-by-step console setup wizard."""

    def __init__(self) -> None:
        self.tv_maze_url = "https://api.tvmaze.com"

    def prompt_media_type(self) -> str:
        """Select between TV Shows and Anime."""
        try:
            media_selection = inquirer.select(
                message="Select Media Type:",
                choices=[{"name": "1. TV Shows", "value": "tv"}, {"name": "2. Anime (Coming Soon)", "value": "anime"}],
                style=custom_style,
            ).execute()

        except KeyboardInterrupt:
            print(f"{Theme.RED}Operation Cancelled.{Theme.RESET}")
            sys.exit(0)

        if media_selection == "anime":
            print(f"{Theme.YELLOW}Anime support is currently under development.{Theme.RESET}")
            sys.exit(1)

        return str(media_selection)

    def prompt_show_name(self) -> str:
        """Get the TV Show name from the user via text prompt."""
        try:
            show_name = inquirer.text(
                message="Search TV Show:",
                style=custom_style,
                validate=lambda text: len(text.strip()) > 0 or "Show name cannot be empty.",
            ).execute()
        except KeyboardInterrupt:
            print(f"{Theme.YELLOW}Anime support is currently under development.{Theme.RESET}")
            sys.exit(0)

        return str(show_name.strip())

    def fetch_show_metadata(self, show_name: str) -> tuple[dict, list[dict]]:
        """Queries TVMaze for the show and returns its metadata and seasons."""
        search_url = f"{self.tv_maze_url}/singlesearch/shows"
        show_response = requests.get(search_url, params={"q": show_name})

        if show_response.status_code == 404:
            print(
                f"{Theme.YELLOW}Error: Could not find any show name {Theme.GREEN}'{show_name}'{Theme.RESET} on TVMaze.{Theme.RESET}"
            )
            sys.exit(1)

        show_data = show_response.json()

        seasons_url = f"{self.tv_maze_url}/shows/{show_data['id']}/seasons"
        seasons_response = requests.get(seasons_url)

        seasons_data = seasons_response.json()

        return show_data, seasons_data

    def fetch_season_episodes(self, season_id: int) -> list[dict[str, Any]]:
        """Queries TVMaze for all episodes belonging to a specific season ID."""
        episodes_url = f"{self.tv_maze_url}/seasons/{season_id}/episodes"
        season_episode_response = requests.get(episodes_url)
        season_episode_data: list[dict[str, Any]] = season_episode_response.json()

        return season_episode_data

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
