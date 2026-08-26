"""Anime File Renaming Controller.

This module provides the orchestrator responsible for mapping local media files
to paginated remote Tenrai API metadata episodes and executing the structural file renaming
operations using continuous or absolute indexing standards typical for Anime.
"""

from pathlib import Path

from metatag.colors import colors, cprint


class AnimeRenamerController:
    """Orchestrates the matching, dry-run display, and final execution mechanics
    for renaming local video files based on paginated Jikan API absolute episode data.
    """

    def __init__(self, target_dir: str, local_files: list[str], episode_manifest: list[str]) -> None:
        self.target_dir = Path(target_dir)
        self.local_files = [Path(f) for f in local_files]
        self.episode_manifest = episode_manifest

    def rename_anime_episodes(self, anime_name: str | None, preview: bool = True) -> None:
        """Pairs local files with remote TV episode manifest and executes the
        renaming operation.
        """
        action_label = "DRY RUN" if preview else "RENAME"
        cprint(
            colors.CYAN,
            f"  [{action_label}] {anime_name} {'[previewing changes only]' if preview else '[applying changes]'}",
        )

        for local_path, remote_name in zip(self.local_files, self.episode_manifest):
            file_extension = local_path.suffix

            # Formulate the clean, new destination path
            new_filename = f"{remote_name}{file_extension}"
            destination_path = self.target_dir / new_filename

            if preview:
                cprint(
                    colors.YELLOW_BOLD_1,
                    f"  {local_path.name}",
                    colors.WHITE_BOLD,
                    "  ",
                    colors.MINT_GREEN_BOLD,
                    f"  {new_filename}",
                )
            else:
                try:
                    source_path = local_path if local_path.is_absolute() else self.target_dir / local_path.name
                    source_path.rename(destination_path)
                    cprint(
                        colors.YELLOW_BOLD_1,
                        f"  {local_path.name}",
                        colors.WHITE_BOLD,
                        "  ",
                        colors.MINT_GREEN_BOLD,
                        f"{new_filename}",
                    )
                except Exception as e:
                    cprint(
                        colors.RED_BOLD,
                        f" Failed to rename the files: {e}",
                    )
