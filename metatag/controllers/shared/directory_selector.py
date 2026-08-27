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
        """Recursively scans and gathers all directories and subdirectories."""
        dirs: list[str] = [base_path]  # Include the root base directory as an option

        for root, subdirs, _ in os.walk(base_path):
            # Sort subdirectories alphabetically for consistent ordering
            subdirs.sort()
            for subdir in subdirs:
                full_path = os.path.join(root, subdir)
                dirs.append(full_path)

        return dirs

    def run(self, media_type: str) -> str:
        """Runs the interactive path selection wizard loop."""

        if media_type == "tv_series":
            base_start_dir = os.path.expanduser("/storage/Tv-Shows/Western")
        elif media_type == "anime_series":
            base_start_dir = os.path.expanduser("/storage/Tv-Shows/Anime")
        else:
            base_start_dir = os.path.expanduser("/storage/Tv-Shows")

        # Scan all directories and subdirectories under base_start_dir
        cprint(colors.CYAN, "Scanning target directories...")
        available_directories = self._get_all_directories(base_start_dir)

        while True:
            target_dir: str = self.base_menu.prompt_target_directory(available_directories)

            is_confirmed = self.base_menu.prompt_confirmation(
                message=f"Proceed with target directory '{target_dir}'?", default=True
            )

            if is_confirmed:
                break

            cprint(colors.YELLOW, "Select alternate directory...")

        return target_dir
