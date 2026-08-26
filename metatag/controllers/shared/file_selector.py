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
        else:
            valid_extensions = ("srt",)

        try:
            all_entries = os.listdir(self.target_dir)
        except OSError as e:
            cprint(colors.RED, f"Failed to read the directory: {e}")
            return []

        selected_files = sorted(
            [
                filename
                for filename in all_entries
                if os.path.isfile(os.path.join(self.target_dir, filename))
                and filename.lower().endswith(valid_extensions)
            ]
        )

        target_dir_items = len(selected_files)

        if not selected_files:
            cprint(colors.YELLOW, f"No matching {file_type_choice} files discovered.")
        else:
            cprint(
                colors.YELLOW_BOLD_UNDERLINE_1,
                f"  Files in directory: {target_dir_items} episodes found",
            )
            # for index, file in enumerate(selected_files, start=1):
            #     cprint(f" {index:02d}. {file}")
            for file in selected_files:
                cprint(colors.YELLOW_BOLD_1, f"  {file}")

            confirmed_files = self.base_menu.prompt_local_file_selection(selected_files)

            if not confirmed_files:
                cprint(colors.YELLOW, "No local files selected. Aborting file selection.")

        return confirmed_files
