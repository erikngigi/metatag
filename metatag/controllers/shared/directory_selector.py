"""Directory Configuration and Traversal Presenter Controller."""

import os
from typing import TYPE_CHECKING

from metatag.colors import colors, cprint

if TYPE_CHECKING:
    from metatag.views.base_menu import BaseMenuView


class DirectoryController:
    """Orchestrates path selection workflows using interactive terminal inputs."""

    def __init__(self, base_menu: "BaseMenuView") -> None:
        self.base_menu = base_menu

    def _get_all_directories(self, base_path: str) -> list[str]:
        """Recursively scans and gathers only leaf subdirectories (directories with no subdirectories)."""
        leaf_dirs: list[str] = []

        for root, subdirs, _ in os.walk(base_path):
            # If subdirs is empty, 'root' is a terminal (leaf) directory
            if not subdirs:
                leaf_dirs.append(root)

        leaf_dirs.sort()
        return leaf_dirs

    def select_directory_for_metadata_embedding(self, media_type: str) -> str:
        """Launches the directory selection wizard for tagging and embedding metadata.

        Args:
            show_name: The target show or series name.
            season_identifier: The season number or identifier.
            media_type: Category of media determining root storage path
                ('tv_series', 'anime_series', etc.).

        Returns:
            str: The absolute path of the target directory selected for metadata embedding.
        """
        if media_type == "tv_series":
            base_start_dir = os.path.expanduser("/storage/Tv-Shows/Western")
        elif media_type == "anime_series":
            base_start_dir = os.path.expanduser("/storage/Tv-Shows/Anime")
        else:
            base_start_dir = os.path.expanduser("/storage/Tv-Shows")

        cprint(colors.CYAN, "Scanning target directories for metadata embedding...")
        available_directories = self._get_all_directories(base_start_dir)

        while True:
            target_dir: str = self.base_menu.prompt_target_directory(available_directories)

            is_confirmed = self.base_menu.prompt_confirmation(
                message=f"Proceed with metadata embedding in: '{target_dir}'?", default=False
            )

            if is_confirmed:
                break

            cprint(colors.YELLOW, "Select alternate directory...")

        return target_dir

    def select_directory_tv_renaming(self, show_name: str, season_identifier: int) -> str:
        """Launches the directory selection wizard for TV Show batch file renaming.

        Returns:
            str: The absolute path of the target directory selected for file renaming.
        """

        base_start_dir = os.path.expanduser("/storage/Tv-Shows/Western")

        cprint(colors.CYAN, "Scanning target directories for file renaming...")
        available_directories = self._get_all_directories(base_start_dir)

        while True:
            target_dir: str = self.base_menu.prompt_target_directory(available_directories)

            is_confirmed = self.base_menu.prompt_confirmation(
                message=f"Proceed with file renaming in: '{target_dir}'?", default=False
            )

            if is_confirmed:
                break

            cprint(colors.YELLOW, "Select alternate directory...")

        return target_dir

    def select_directory_anime_renaming(self, show_name: str) -> str:
        """Launches the directory selection wizard for Anime batch file renaming.

        Returns:
            str: The absolute path of the target directory selected for file renaming.
        """

        base_start_dir = os.path.expanduser("/storage/Tv-Shows/Anime")

        cprint(colors.CYAN, "Scanning target directories for file renaming...")
        available_directories = self._get_all_directories(base_start_dir)

        while True:
            target_dir: str = self.base_menu.prompt_target_directory(available_directories)

            is_confirmed = self.base_menu.prompt_confirmation(
                message=f"Proceed with file renaming in: '{target_dir}'?", default=False
            )

            if is_confirmed:
                break

            cprint(colors.YELLOW, "Select alternate directory...")

        return target_dir
