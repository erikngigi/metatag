"""TV Series File Renaming Controller.

This module provides the orchestrator responsible for mapping local media files
to remote TVMaze metadata episodes and executing the structural file renaming operations
specifically tailored for standard western television formats.
"""

from pathlib import Path

from metatag.colors import colors, cprint


class TVRenamerController:
    """Orchestrates the matching, dry-run display, and final execution mechanics
    for renaming local video files based on TVMaze season manifest data.
    """

    def __init__(self, target_dir: str, local_files: list[str], episode_manifest: list[str]) -> None:
        self.target_dir = Path(target_dir)
        self.local_files = [Path(f) for f in local_files]
        self.episode_manifest = episode_manifest

    def rename_tv_episodes(self, show_name: str, season: int, dry_run: bool = True) -> None:
        """Pairs local files with remote TV episode manifest and executes the
        renaming operation.
        """
        action_label = "DRY RUN" if dry_run else "RENAME"
        cprint(
            colors.CYAN,
            f"\n[{action_label}] {show_name} Season {season} {'[previewing changes only]' if dry_run else '[applying changes]'}",
        )

        for local_path, remote_name in zip(self.local_files, self.episode_manifest):
            file_extension = local_path.suffix

            # Formulate the clean, new destination path
            new_filename = f"{remote_name}{file_extension}"
            destination_path = self.target_dir / new_filename

            if dry_run:
                cprint(colors.WHITE, f" {local_path.name}", colors.YELLOW, "    ", colors.CYAN, f"{new_filename}")
            else:
                try:
                    source_path = local_path if local_path.is_absolute() else self.target_dir / local_path.name
                    source_path.rename(destination_path)
                    cprint(
                        colors.WHITE,
                        f" {local_path.name}",
                        colors.YELLOW,
                        "    ",
                        colors.GREEN,
                        f"{new_filename}",
                        colors.GREEN,
                        " [renamed]",
                    )
                except Exception as e:
                    cprint(
                        colors.WHITE,
                        f" {local_path.name}",
                        colors.YELLOW,
                        "    ",
                        colors.GREEN,
                        f"{new_filename}",
                        colors.GREEN,
                        f" [failed: {e}]",
                    )
