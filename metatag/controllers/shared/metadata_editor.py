"""Universal Header Title Editor Controller for MKV and MP4 formats."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, List

from metatag.colors import colors, cprint
from metatag.controllers.shared.directory_selector import DirectoryController
from metatag.controllers.shared.file_selector import FileSelectorController

if TYPE_CHECKING:
    from metatag.views.base_menu import BaseMenuView


class MetadataController:
    """Orchestrates updating internal metadata titles using mkvpropedit and tageditor."""

    def __init__(self, base_menu: BaseMenuView) -> None:
        self.base_menu = base_menu

    def cleanup_bak_files(self, target_dir: str) -> None:
        """Finds and removes any .bak backup files created by tageditor."""
        try:
            bak_files = [f for f in os.listdir(target_dir) if f.lower().endswith(".bak")]
            if not bak_files:
                return

            cprint(colors.CYAN, f"\nCleaning up {len(bak_files)} temporary backup file(s)...")
            for bak in bak_files:
                os.remove(os.path.join(target_dir, bak))
                cprint(colors.YELLOW, f"  Removed: {bak}")
        except OSError as e:
            cprint(colors.RED, f"Failed during .bak file cleanup: {e}")

    def run(self, media_type: str = "general") -> None:
        """Runs the interactive metadata editing workflow."""
        # 1. Select directory
        dir_controller = DirectoryController(self.base_menu)
        target_dir = dir_controller.run(media_type=media_type)

        if not target_dir:
            return

        # 2. Select local files
        file_selector = FileSelectorController(self.base_menu, target_dir)
        confirmed_files: List[str] = file_selector.run()

        if not confirmed_files:
            return

        cprint(
            colors.MINT_GREEN_BOLD,
            "\nUpdating title metadata for the files:",
        )

        success_count = 0
        has_mp4 = False

        # 3. Process each file based on its extension
        for index, filename in enumerate(confirmed_files, start=1):
            file_path = os.path.join(target_dir, filename)
            title_name = Path(filename).stem
            ext = Path(filename).suffix.lower()

            if ext == ".mkv":
                if shutil.which("mkvpropedit") is None:
                    cprint(
                        colors.RED, f"  [{index:02d}/{len(confirmed_files):02d}] Error: 'mkvpropedit' binary missing."
                    )
                    continue
                cmd = ["mkvpropedit", file_path, "--edit", "info", "--set", f"title={title_name}"]

            elif ext == ".mp4":
                if shutil.which("tageditor") is None:
                    cprint(colors.RED, f"  [{index:02d}/{len(confirmed_files):02d}] Error: 'tageditor' binary missing.")
                    continue
                has_mp4 = True
                cmd = ["tageditor", "-s", f"title={title_name}", "-f", file_path]

            else:
                cprint(
                    colors.YELLOW, f"  [{index:02d}/{len(confirmed_files):02d}] Skipping unsupported format: {filename}"
                )
                continue

            try:
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                cprint(
                    colors.GREEN,
                    f"  [{index:02d}/{len(confirmed_files):02d}] Updated title: '{title_name}' -> {filename}",
                )
                success_count += 1
            except subprocess.CalledProcessError as e:
                cprint(
                    colors.RED, f"  [{index:02d}/{len(confirmed_files):02d}] Failed '{filename}': {e.stderr.strip()}"
                )

        cprint(
            colors.MINT_GREEN_BOLD,
            f"\nFinished metadata updates. Successfully updated {success_count}/{len(confirmed_files)} files.",
        )

        # 4. Clean up .bak files if MP4 files were processed
        if has_mp4:
            self.cleanup_bak_files(target_dir)
