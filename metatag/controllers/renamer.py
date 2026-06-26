"""Local Filesystem Renaming and Matching Engine Controller."""

from __future__ import annotations

import os

from metatag.views.theme import Theme


class FileRenamerController:
    """Orchestrates matching local tracking media files with remote API metadata payloads."""

    def __init__(self, target_dir: str, local_files: list[str], remote_episodes: list[str]) -> None:
        self.target_dir = target_dir
        self.local_files = local_files
        self.remote_episodes = remote_episodes

    def execute_rename(self, show_name: str, season_num: int, dry_run: bool = False) -> None:
        """Matches local file numbers to remote metadata lists and alters names on disk."""
        if not self.local_files:
            print(f"{Theme.YELLOW}[!] No files provided for renaming module execution.{Theme.RESET}")
            return

        if len(self.local_files) != len(self.remote_episodes):
            print(
                f"{Theme.BOLD}{Theme.RED}[] Critial Error: Count mismatch detected!{Theme.RESET}\n"
                f"{Theme.YELLOW}Local files: {len(self.local_files)} -- API episodes: {len(self.remote_episodes)}\n"
                f"Execution aborted to prevent corrupted indexing.{Theme.RESET}"
            )
            return

        print(f"\n{Theme.BOLD}{Theme.YELLOW}Renaming {show_name} Season {season_num}{Theme.RESET}\n")

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

                print(f"{Theme.GREY}{old_filename}{Theme.RESET} -> {Theme.GREEN}{new_filename}{Theme.RESET}")

                if not dry_run:
                    try:
                        os.rename(old_path, new_path)
                        renamed_count += 1
                    except OSError as e:
                        print(f"{Theme.RED}System error execution failure: {e}{Theme.RESET}")
            else:
                print(
                    f"{Theme.YELLOW}Warning: No matching remote metadata index found for: {old_filename}{Theme.RESET}"
                )

        print(
            f"\n{Theme.GREEN}Renaming execution cycle finalized! Successfully altered {renamed_count} asset file paths.{Theme.RESET}"
        )
