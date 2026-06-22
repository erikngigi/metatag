"""Directory Configuration and Traversal Presenter Controller."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

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

        # 1. Capture the source folder using auto-suggest pathing
        target_dir = self.wizard.prompt_target_directory(base_start_dir)

        return target_dir
