"""Directory Configuration and Traversal Presenter Controller."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.views.interactive import InteractiveWizard


class DirectoryController:
    """Orchestrates path selection workflows using interactive terminal inputs."""

    def __init__(self, wizard: InteractiveWizard) -> None:
        self.wizard = wizard

    def run(self) -> str:
        """Runs the interactive path selection wizard loop."""

        # Define your base start directory explicitly (e.g., Linux Home directory or CWD)
        base_start_dir = os.path.expanduser("/storage/Tv-Shows")  # Resolves to /home/eric

        while True:
            target_dir = self.wizard.prompt_target_directory(base_start_dir)

            is_confirmed = self.wizard.prompt_confirmation(
                message=f"Proceed with target directory '{target_dir}'?", default=True
            )

            if is_confirmed:
                break

            print(f"{Theme.YELLOW}Select alternate directory..{Theme.RESET}")

        return target_dir
