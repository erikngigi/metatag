"""Directory Configuration and Traversal Presenter Controller."""

import os
from typing import TYPE_CHECKING

from metatag.colors import colors, cprint

if TYPE_CHECKING:
    from metatag.views.base_menu import BaseMenuView


class DirectoryController:
    """Orchestrates path selection workflows using interactive terminal inputs."""

    def __init__(self, base_menu: BaseMenuView) -> None:
        self.base_menu = base_menu

    def run(self) -> str:
        """Runs the interactive path selection wizard loop."""

        # Define your base start directory explicitly (e.g., Linux Home directory or CWD)
        base_start_dir = os.path.expanduser("/storage/Tv-Shows")  # Resolves to /home/eric

        while True:
            target_dir: str = self.base_menu.prompt_target_directory(base_start_dir)

            is_confirmed = self.base_menu.prompt_confirmation(
                message=f"Proceed with target directory '{target_dir}'?", default=True
            )

            if is_confirmed:
                break

            cprint(colors.YELLOW, "Select alternate directory...")

        return target_dir
