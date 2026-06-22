"""Local Filesystem Scanning and Filtering Engine.

Acts as part of the Model layer. This module encapsulates file system
traversal, extension filtering, and path validation logic. It isolates
disk interaction entirely from console output or application state flows.
"""

from __future__ import annotations

from pathlib import Path


class FileScanner:
    """Local filesystem scanning and discovery engine.

    Acts as part of the Model layer in the MVC architectural pattern. This
    class encapsulates directory traversal, extension filtering, and path
    validation logic, fully isolating low-level disk interaction from console
    output or application controller workflows.
    """

    def __init__(self, target_dir: str, recursive: bool, videos_only: bool, subtitles_only: bool):
        """
        Model responsible for disk discovery and traversal handling.
        """
        self.target_dir = Path(target_dir)
        self.recursive = recursive

        # Common video extensions
        VIDEO_EXTENSIONS = {"mkv", "mp4", "avi", "mov"}

        # Common subtitle extensions
        SUBTITLE_EXTENSIONS = {"srt"}

        # Determine allowed extensions (stripping the leading dot for clean comparison)
        if videos_only:
            self.allowed_extensions = VIDEO_EXTENSIONS
        elif subtitles_only:
            self.allowed_extensions = SUBTITLE_EXTENSIONS
        else:
            self.allowed_extensions = VIDEO_EXTENSIONS | SUBTITLE_EXTENSIONS

    def is_valid_directory(self) -> bool:
        """Checks if the target path is a valid local directory."""
        pass
        return self.target_dir.exists() and self.target_dir.is_dir()

    def scan_files(self) -> list[Path]:
        """
        Traverses the file-system and returns a filtered list of Path objects.
        """

        # Select appropriate pathlib generator strategy
        search_generator = self.target_dir.rglob("*") if self.recursive else self.target_dir.glob("*")

        files = []
        for item in search_generator:
            if item.is_file() and item.suffix.lower().lstrip(".") in self.allowed_extensions:
                files.append(item)

        return files
