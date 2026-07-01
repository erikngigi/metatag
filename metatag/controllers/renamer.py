"""Local Filesystem Renaming and Matching Engine Controller."""

from __future__ import annotations

import os

from metatag.colors import colors, cprint


class FileRenamerController:
    """Orchestrates matching local tracking media files with remote API metadata payloads."""

    def __init__(self, target_dir: str, local_files: list[str], remote_episodes: list[str]) -> None:
        self.target_dir = target_dir
        self.local_files = local_files
        self.remote_episodes = remote_episodes

    def execute_rename(self, show_name: str, season_num: int, dry_run: bool = False) -> None:
        """Matches local file numbers to remote metadata lists and alters names on disk."""
        if not self.local_files:
            cprint(colors.YELLOW, "No files provided for renaming module execution.")
            return

        if len(self.local_files) != len(self.remote_episodes):
            cprint(
                colors.YELLOW,
                "Critial Error: Count mismatch detected!\n"
                f"Local files: {len(self.local_files)} -- API episodes: {len(self.remote_episodes)}\n"
                f"Execution aborted to prevent corrupted indexing.",
            )
            return

        cprint(colors.YELLOW, f"Renaming {show_name} Season {season_num}.\n")

        # Track successful adjustments
        renamed_count = 0

        # Loop through local files and attempt a strict index alignment map
        for index, old_filename in enumerate(self.local_files):
            # Extract extension (.mp4, .mkv, .srt) dynamically
            name_part, extension = os.path.splitext(old_filename)

            # Check if we have a matching remote API episode entry for this positional sequence
            if index < len(self.remote_episodes):
                # 2. Extract title directly as a string
                ep_title = self.remote_episodes[index]

                # Standardize name structure: "01 - Episode Title.ext"
                new_filename = f"{ep_title}{extension}"

                # Generate full absolute filesystem paths
                old_path = os.path.join(self.target_dir, old_filename)
                new_path = os.path.join(self.target_dir, new_filename)

                cprint(colors.CYAN, f"{old_filename} -> {new_filename}")

                if not dry_run:
                    try:
                        os.rename(old_path, new_path)
                        renamed_count += 1
                    except OSError as e:
                        cprint(colors.RED, f"System error execution failure: {e}")
            else:
                cprint(colors.YELLOW, f"Warning: No matching remote metadata index found for: {old_filename}.")

        cprint(f"\nRenaming execution cycle finalized! Successfully altered {renamed_count} asset file paths.")
