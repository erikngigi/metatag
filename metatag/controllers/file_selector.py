"""Local File Ingestion and Extension Filtering Controller."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.views.interactive import InteractiveWizard


class FileSelectorController:
    """Orchestrates gathering user filtering intent and scanning local storage."""

    def __init__(self, wizard: InteractiveWizard, target_dir: str) -> None:
        self.wizard = wizard
        self.target_dir = target_dir

    def run(self) -> list[str]:
        """Runs the interactive file selection loop and maps active matches."""
        file_type_choice = self.wizard.prompt_rename_type()

        if file_type_choice == "video":
            valid_extensions: tuple[str, ...] = ("mkv", "mp4")
            print(f"\n{Theme.CYAN}Scanning strictly for Video Assests (.mp4, .mkv){Theme.RESET}.")
        else:
            valid_extensions = ("srt",)
            print(f"\n{Theme.CYAN}Scanning strictly for Subtitle Tracking Assests. (.srt){Theme.RESET}.")

        try:
            all_entries = os.listdir(self.target_dir)
        except OSError as e:
            print(f"{Theme.RED}Failed to read directory: {e}{Theme.RESET}")
            return []

        selected_files = [
            filename
            for filename in all_entries
            if os.path.isfile(os.path.join(self.target_dir, filename)) and filename.lower().endswith(valid_extensions)
        ]

        selected_files.sort()

        if not selected_files:
            print(f"{Theme.YELLOW}No matching {file_type_choice} files discovered in the workspace.{Theme.RESET}")
        else:
            print(f"{Theme.GREEN}Succesfully indexed {len(selected_files)} target files(s):{Theme.RESET}")
            for index, file in enumerate(selected_files, start=1):
                print(f"  {index:02d}. {file}")

        return selected_files
