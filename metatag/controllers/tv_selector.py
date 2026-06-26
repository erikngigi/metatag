"""TV Series Metadata Selector Controller."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.views.theme import Theme

if TYPE_CHECKING:
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
                show_title: str = show["name"]
                language: str = show["language"]
                status: str = show["status"]

                premiered_raw: str = show.get("premiered") or ""
                ended_raw: str = show.get("ended") or ""

                start_year = premiered_raw.split("-")[0] if premiered_raw else "TBA"

                if status.lower() == "running":
                    year_range = f"{start_year} - Present"
                else:
                    end_year = ended_raw.split("-")[0] if ended_raw else "TBA"
                    year_range = f"{start_year} - {end_year}"

                label = f"{show_title} ({year_range})   {language} [{status}]"
                show_choices.append({"name": label, "value": show})

            selected_show = self.wizard.prompt_show_selection(show_choices)
            show_id: int = selected_show["id"]
            show_matched_title: str = selected_show["name"]

            # Step 4: Fetch and selected seasons
            seasons_choices = self.tvmaze.fetch_show_seasons(show_id)
            if not seasons_choices:
                print(f"{Theme.YELLOW}No seasons found for this show. Please try again.{Theme.RESET}")
                continue

            selected_season = self.wizard.prompt_season_selection(seasons_choices)
            season_id: int = selected_season["id"]
            season_number: int = selected_season["number"]

            # Step 5: Fetch episode manifest of each season
            selected_season_episodes = self.tvmaze.fetch_season_episodes_names(season_id, show_matched_title)
            if not selected_season_episodes:
                print(f"{Theme.YELLOW}No episodes found for {show_name} Season {season_number}.{Theme.RESET}")
                continue

            season_episode_names = []
            for episodes in selected_season_episodes:
                season_episode_names.append(episodes["name"])

            self.wizard.display_episode_manifest(season_episode_names)

            # Step 6: Loop control
            next_action = self.wizard.prompt_metadata_checkpoint()

            if next_action == "restart":
                print(f"{Theme.CYAN}Restarting Metatag Wizard.{Theme.RESET}")
                self.wizard.clear_screen()
                continue

            break

        return show_matched_title, season_number, season_episode_names
