"""Local File Ingestion and Extension Filtering Controller."""

from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from metatag.colors import color, colors, cprint

if TYPE_CHECKING:
    from metatag.views.base_menu import BaseMenuView


_NATURAL_SPLIT = re.compile(r"(\d+)")


def _natural_sort_key(filename: str) -> list:
    """Splits a filename into text/number chunks so '2' sorts before '10'.

    Plain lexical sort would order 'E1, E10, E2' -- which silently misaligns the
    local-file <-> remote-episode pairing done by zip() in AnimeRenamerController,
    since the episode manifest is built in true numeric order.
    """
    return [int(chunk) if chunk.isdigit() else chunk.lower() for chunk in _NATURAL_SPLIT.split(filename)]


class FileSelectorController:
    """Orchestrates gathering user filtering intent and scanning local storage."""

    def __init__(self, base_menu: BaseMenuView, target_dir: str) -> None:
        self.base_menu = base_menu
        self.target_dir = target_dir

    def run(self) -> list[str]:
        """Runs the interactive file selection loop and maps active matches."""
        file_type_choice = self.base_menu.prompt_filetype_rename()

        if file_type_choice == "video":
            valid_extensions: tuple[str, ...] = (".mkv", ".mp4")
        else:
            valid_extensions = (".srt",)

        try:
            all_entries = os.listdir(self.target_dir)
        except OSError as e:
            cprint(colors.RED, f"Failed to read the directory: {e}")
            return []

        matched_files = [
            filename
            for filename in all_entries
            if os.path.isfile(os.path.join(self.target_dir, filename))
            and os.path.splitext(filename)[1].lower() in valid_extensions
        ]

        selected_files = sorted(matched_files, key=_natural_sort_key)
        target_dir_items = len(selected_files)

        if not selected_files:
            cprint(colors.YELLOW, f"No matching {file_type_choice} files discovered.")
            return []

        cprint(colors.MINT_GREEN_BOLD, f"\n  Files in directory: {target_dir_items} episodes found")

        for index, file in enumerate(selected_files, start=1):
            cprint(colors.YELLOW_BOLD_1, f"  [{index:02d}/{target_dir_items:02d}] {file}")
        cprint()

        confirmed_files = self.base_menu.prompt_local_file_selection(selected_files)

        if not confirmed_files:
            cprint(colors.YELLOW, "No local files selected. Aborting file selection.")

        return confirmed_files
