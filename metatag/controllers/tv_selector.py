"""TV Series Metadata Selector Controller."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.models.schemas.tvmaze import TVEpisodeSchema, TVSeasonSchema, TVShowSchema
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.interactive import InteractiveWizard


class TVSelectorController:
    """Manages the interactive selection loop specifically for TV series using TVMaze API."""

    def __init__(self, wizard: InteractiveWizard, tvmaze: TVMazeModel) -> None:
        self.wizard = wizard
        self.tvmaze = tvmaze

    def execute(self) -> tuple[str, int, list[Any]]:
        """Executes the step-by-step TV selection pipeline."""
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
                    return selected_show.name, selected_season.number, season_episode_names

                elif next_action == "alternate_season":
                    self.wizard.clear_screen()
                    print(f"{Theme.CYAN}Reloading Seasons List for {selected_show.name}.{Theme.RESET}")
                    continue

                elif next_action == "search_again":
                    self.wizard.clear_screen()
                    print(f"{Theme.GREY}Search for TV Show{Theme.RESET}")
                    break
