"""Local File Ingestion and Extension Filtering Controller."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from metatag.colors import colors, cprint

if TYPE_CHECKING:
    from metatag.views.base_menu import BaseMenuView


class FileSelectorController:
    """Orchestrates gathering user filtering intent and scanning local storage."""

    def __init__(self, base_menu: BaseMenuView, target_dir: str) -> None:
        self.base_menu = base_menu
        self.target_dir = target_dir

    def run(self) -> list[str]:
        """Runs the interactive file selection loop and maps active matches."""
        file_type_choice = self.base_menu.prompt_filetype_rename()

        if file_type_choice == "video":
            valid_extensions: tuple[str, ...] = ("mkv", "mp4")
            cprint(colors.CYAN, "Scanning strictly for video assets. ('mp4', 'mkv')")
        else:
            valid_extensions = ("srt",)
            cprint(colors.CYAN, "Scanning strictly for subtitle assets. ('srt')")

        try:
            all_entries = os.listdir(self.target_dir)
        except OSError as e:
            cprint(colors.RED, f"Failed to read the directory: {e}")
            return []

        selected_files = [
            filename
            for filename in all_entries
            if os.path.isfile(os.path.join(self.target_dir, filename)) and filename.lower().endswith(valid_extensions)
        ]

        selected_files.sort()

        if not selected_files:
            cprint(colors.YELLOW, f"No matching {file_type_choice} files discovered.")
        else:
            cprint(colors.GREEN, f"Succesfully indexed {len(selected_files)} target files:")
            for index, file in enumerate(selected_files, start=1):
                cprint(f" {index:02d}. {file}")

        return selected_files
