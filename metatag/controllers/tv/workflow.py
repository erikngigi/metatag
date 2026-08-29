"""TV Series Metadata Selector Controller."""

from typing import TYPE_CHECKING, Any

# Imported local pipeline controllers directly into the sub-module context
from metatag.colors import colors, cprint
from metatag.controllers.shared.directory_selector import DirectoryController
from metatag.controllers.shared.file_selector import FileSelectorController
from metatag.controllers.tv.renamer import TVRenamerController

if TYPE_CHECKING:
    from metatag.models.schemas.tvmaze import TVSeasonSchema, TVShowSchema
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.base_menu import BaseMenuView
    from metatag.views.tv_menu import TVMenuView


class TVSelectorController:
    """Manages the interactive selection loop specifically for TV series using TVMaze API."""

    def __init__(self, base_menu: BaseMenuView, tvmaze: TVMazeModel, tvmenu: TVMenuView) -> None:
        self.base_menu = base_menu
        self.tvmaze = tvmaze
        self.tvmenu = tvmenu

    def execute(self, cli_args: Any) -> None:
        """Executes the complete step-by-step TV selection and renaming pipeline."""
        while True:
            # Step 1: Get show name from the user
            show_name = self.tvmenu.prompt_show_name()

            # Step 2: Fuzzy search using TVMaze Model
            fuzzy_search_shows = self.tvmaze.fuzzy_search_show(show_name)

            if not fuzzy_search_shows:
                cprint(colors.YELLOW, f"No shows found matching the pattern '{show_name}'.")
                continue

            # Step 3: Format and prompt for show selection
            show_choices = []
            for show in fuzzy_search_shows:
                label = f"{show.name} ({show.year_range})"
                show_choices.append({"name": label, "value": show})

            selected_show: TVShowSchema = self.tvmenu.prompt_show_selection(show_choices)

            while True:
                # Step 4: Fetch and selected seasons
                seasons_list = self.tvmaze.fetch_show_seasons(selected_show.id)

                if not seasons_list:
                    cprint(colors.YELLOW, "No season/seasons found for this show.")
                    break

                season_choices = []
                for season in seasons_list:
                    choice = {"name": season.summary_label, "value": season}
                    season_choices.append(choice)

                selected_season: TVSeasonSchema = self.tvmenu.prompt_season_selection(season_choices)

                # Step 5: Fetch episode manifest of each season
                selected_season_episodes_list = self.tvmaze.fetch_season_episodes_names(selected_season.id)

                if not selected_season_episodes_list:
                    cprint(colors.YELLOW, f"No episodes found for {selected_show.name}.")
                    continue

                season_episode_names: list[str] = []
                for episode in selected_season_episodes_list:
                    label = f"{selected_show.name} {episode.marker} - {episode.name}"
                    season_episode_names.append(label)

                # self.base_menu.print_episodes(season_episode_names)
                self.tvmenu.print_tv_episode_manifest(selected_show.name, selected_season.number, season_episode_names)

                # Step 6: Loop control
                next_action = self.tvmenu.prompt_tv_post_manifest_action()

                if next_action == "rename":
                    dir_controller = DirectoryController(self.base_menu)
                    target_dir = dir_controller.select_directory_tv_renaming(selected_show.name, selected_season.number)

                    file_controller = FileSelectorController(self.base_menu, target_dir)
                    files_to_process = file_controller.run()

                    if not files_to_process:
                        cprint(colors.YELLOW, "\n  No files selected for processing. Returning to season menu...\n")
                        continue

                    tv_renamer = TVRenamerController(
                        self.base_menu,
                        target_dir=target_dir,
                        local_files=files_to_process,
                        episode_manifest=season_episode_names,
                    )

                    if files_to_process:
                        # Explicit --dry-run flag: preview only, no confirmation needed
                        if getattr(cli_args, "preview", False):
                            tv_renamer.rename_tv_episodes(
                                show_name=selected_show.name, season=selected_season.number, preview=True
                            )
                        else:
                            tv_renamer.rename_tv_episodes(
                                show_name=selected_show.name, season=selected_season.number, preview=True
                            )

                            proceed = self.base_menu.prompt_confirmation(
                                message="Do you want to proceed with renaming these files?",
                                default=False,
                            )

                            if not proceed:
                                cprint(colors.YELLOW, "Renaming sequence aborted by user. No files were changed.")
                                return

                            tv_renamer.rename_tv_episodes(
                                show_name=selected_show.name, season=selected_season.number, preview=cli_args.preview
                            )
                        return

                elif next_action == "alternate_season":
                    self.base_menu.clear_screen()
                    cprint(colors.CYAN, f"Reloading {selected_show.name} seasons list.")
                    continue

                elif next_action == "search_again":
                    self.base_menu.clear_screen()
                    cprint(colors.CYAN_BOLD, "Search for TV Show.")
                    break
