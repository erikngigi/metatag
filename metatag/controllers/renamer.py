"""Local Filesystem Renaming and Matching Engine Controller."""

from __future__ import annotations

import os

from metatag.views.theme import Theme


class FileRenamerController:
    """Orchestrates matching local tracking media files with remote API metadata payloads."""

    def __init__(self, target_dir: str, local_files: list[str], remote_episodes: list[dict]) -> None:
        self.target_dir = target_dir
        self.local_files = local_files
        self.remote_episodes = remote_episodes

    def execute_rename(self, show_name: str, season_num: int, dry_run: bool = False) -> None:
        """Matches local file numbers to remote metadata lists and alters names on disk."""
        if not self.local_files:
            print(f"{Theme.YELLOW}[!] No files provided for renaming module execution.{Theme.RESET}")
            return

        print(f"\n{Theme.BOLD}{Theme.YELLOW}--- Starting Renaming Operations Pipeline ---{Theme.RESET}\n")

        # Track successful adjustments
        renamed_count = 0

        # Loop through local files and attempt a strict index alignment map
        for index, old_filename in enumerate(self.local_files):
            # Extract extension (.mp4, .mkv, .srt) dynamically
            name_part, extension = os.path.splitext(old_filename)

            # Check if we have a matching remote API episode entry for this positional sequence
            if index < len(self.remote_episodes):
                episode_data = self.remote_episodes[index]
                ep_num = episode_data.get("number")
                ep_title = episode_data.get("name")

                # Format the fallback token placeholders cleanly if data properties are empty
                ep_str = f"{ep_num:02d}" if ep_num is not None else f"{index + 1:02d}"
                clean_title = ep_title.replace("/", "-").strip() if ep_title else "Unknown Title"

                # Standardize name structure: "Show Name - S01E01 - Episode Title.ext"
                # new_filename = f"{show_name} - S{season_num:02d}{ep_str} - {clean_title}{extension}"
                new_filename = f"{ep_str} - {clean_title}{extension}"

                # Generate full absolute filesystem paths
                old_path = os.path.join(self.target_dir, old_filename)
                new_path = os.path.join(self.target_dir, new_filename)

                print(f"{Theme.GREY}From:{old_filename}{Theme.RESET}")
                print(f"{Theme.GREEN}To:{new_filename}{Theme.RESET}")

                if not dry_run:
                    try:
                        os.rename(old_path, new_path)
                        renamed_count += 1
                    except OSError as e:
                        print(f"{Theme.RED}[!] System error execution failure: {e}{Theme.RESET}")
                else:
                    print(f"{Theme.CYAN}[Preview Mode] No alterations executed on disk.{Theme.RESET}")
            else:
                print(
                    f"{Theme.YELLOW}[!] Warning: No matching remote metadata index found for: {old_filename}{Theme.RESET}"
                )

        print(
            f"\n{Theme.GREEN}[✔] Renaming execution cycle finalized! Successfully altered {renamed_count} asset file paths.{Theme.RESET}"
        )
