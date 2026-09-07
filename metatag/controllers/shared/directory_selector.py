"""Directory Configuration and Traversal Presenter Controller."""

from typing import TYPE_CHECKING

from metatag.colors import colors, cprint

if TYPE_CHECKING:
    from metatag.views.base_menu import BaseMenuView


class DirectoryController:
    """Orchestrates path selection workflows using interactive terminal inputs."""

    def __init__(self, base_menu: "BaseMenuView") -> None:
        self.base_menu = base_menu

    def _navigate_and_confirm(self, start_path: str, message: str) -> str:
        """Lets the user freely navigate to a directory, then confirms before returning it.

        `start_path` only seeds the prompt -- the user can tab-complete deeper,
        or clear it and type an entirely different root (e.g. swap '/storage/'
        for '/home/') before landing on a final choice.
        """
        while True:
            target_dir = self.base_menu.prompt_directory_path(start_path=start_path, message=message)

            is_confirmed = self.base_menu.prompt_confirmation(message=f"Proceed with: '{target_dir}'?", default=False)

            if is_confirmed:
                return target_dir

            cprint(colors.YELLOW, "Select alternate directory...")
            # Resume navigation from wherever they last landed, not back at the original root.
            start_path = target_dir

    def select_directory_for_metadata_embedding(self, media_type: str) -> str:
        """Launches the directory navigation wizard for tagging and embedding metadata.

        Args:
            media_type: Category of media determining the starting root path
                ('tv_series', 'anime_series', etc.). The user can navigate away
                from this starting point to anywhere on the filesystem.

        Returns:
            str: The absolute path of the target directory selected for metadata embedding.
        """
        if media_type == "tv_series":
            base_start_dir = "/storage/Tv-Shows/Western/"
        elif media_type == "anime_series":
            base_start_dir = "/storage/Tv-Shows/Anime/"
        else:
            base_start_dir = "/storage/Tv-Shows/"

        cprint(colors.CYAN, "Navigate to the target directory for metadata embedding...")
        return self._navigate_and_confirm(base_start_dir, "Select the target directory:")

    def select_directory_tv_renaming(self, show_name: str, season_identifier: int) -> str:
        """Launches the directory navigation wizard for TV Show batch file renaming.

        Returns:
            str: The absolute path of the target directory selected for file renaming.
        """
        cprint(colors.CYAN, "Navigate to the target directory for file renaming...")
        return self._navigate_and_confirm("/storage/Tv-Shows/Western/", "Select the target directory:")

    def select_directory_anime_renaming(self, show_name: str) -> str:
        """Launches the directory navigation wizard for Anime batch file renaming.

        Returns:
            str: The absolute path of the target directory selected for file renaming.
        """
        cprint(colors.CYAN, "Navigate to the target directory for file renaming...")
        return self._navigate_and_confirm("/storage/Tv-Shows/Anime/", "Select the target directory:")
