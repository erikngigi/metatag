"""TV Series Metadata Selector Controller."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Imported local pipeline controllers directly into the sub-module context
from metatag.controllers.directory_selector import DirectoryController
from metatag.controllers.file_selector import FileSelectorController
from metatag.controllers.renamer import FileRenamerController
from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.models.schemas.tvmaze import TVSeasonSchema, TVShowSchema
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.interactive import InteractiveWizard


class TVSelectorController:
    """Manages the interactive selection loop specifically for TV series using TVMaze API."""

    def __init__(self, wizard: InteractiveWizard, tvmaze: TVMazeModel) -> None:
        self.wizard = wizard
        self.tvmaze = tvmaze

    def execute(self, args: Any) -> None:
        """Executes the complete step-by-step TV selection and renaming pipeline."""
        while True:
            # Step 1: Get show name from the user
            show_name = self.wizard.prompt_show_name()

            # Step 2: Fuzzy search using TVMaze Model
            fuzzy_search_shows = self.tvmaze.fuzzy_search_show(show_name)

            if not fuzzy_search_shows:
                print(f"{Theme.YELLOW}No shows found matching '{show_name}'. Please try again.{Theme.RESET}")
                continue

            # Step 3: Format and prompt for show selection
            show_choices = []
            for show in fuzzy_search_shows:
                label = f"󰑈 {show.name} ({show.year_range})   {show.language} [{show.status}]"
                show_choices.append({"name": label, "value": show})

            selected_show: TVShowSchema = self.wizard.prompt_show_selection(show_choices)

            while True:
                # Step 4: Fetch and selected seasons
                seasons_list = self.tvmaze.fetch_show_seasons(selected_show.id)

                if not seasons_list:
                    print(f"{Theme.YELLOW}No seasons found for this show. Please try again.{Theme.RESET}")
                    break

                season_choices = []
                for season in seasons_list:
                    choice = {"name": season.summary_label, "value": season}
                    season_choices.append(choice)

                selected_season: TVSeasonSchema = self.wizard.prompt_season_selection(season_choices)

                # Step 5: Fetch episode manifest of each season
                selected_season_episodes_list = self.tvmaze.fetch_season_episodes_names(selected_season.id)

                if not selected_season_episodes_list:
                    print(
                        f"{Theme.YELLOW}No episodes found for {selected_show.name} Season {selected_season.number}.{Theme.RESET}"
                    )
                    continue

                season_episode_names: list[str] = []
                for episode in selected_season_episodes_list:
                    label = f"{selected_show.name} {episode.marker} - {episode.name}"
                    season_episode_names.append(label)

                self.wizard.display_episode_manifest(season_episode_names)

                # Step 6: Loop control
                next_action = self.wizard.prompt_metadata_checkpoint()

                if next_action == "rename":
                    print(f"\nStart renaming process for {selected_show.name} season {selected_season.number}.\n")

                    # ─── DECENTRALIZED PIPELINES B, C, & D EXECUTED HERE ───
                    dir_controller = DirectoryController(self.wizard)
                    target_dir = dir_controller.run()

                    file_controller = FileSelectorController(self.wizard, target_dir)
                    files_to_process = file_controller.run()

                    if files_to_process:
                        renamer = FileRenamerController(
                            target_dir=target_dir, local_files=files_to_process, remote_episodes=season_episode_names
                        )

                        # Dry run check
                        renamer.execute_rename(
                            show_name=selected_show.name, season_num=selected_season.number, dry_run=True
                        )

                        if self.wizard.prompt_rename_confirmation():
                            renamer.execute_rename(
                                show_name=selected_show.name, season_num=selected_season.number, dry_run=args.dry_run
                            )
                            return  # Break completely out of the selection loop on successful execution
                        else:
                            print(
                                f"{Theme.YELLOW}Renaming sequence aborted by user. No files were changed.{Theme.RESET}"
                            )
                    return

                elif next_action == "alternate_season":
                    self.wizard.clear_screen()
                    print(f"{Theme.CYAN}Reloading Seasons List for {selected_show.name}.{Theme.RESET}")
                    continue

                elif next_action == "search_again":
                    self.wizard.clear_screen()
                    print(f"{Theme.GREY}Search for TV Show{Theme.RESET}")
                    break
