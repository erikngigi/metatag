"""API Metadata Information Presenter Controller.

Coordinates the data flow between the InteractiveWizard view/client engine
and formats the resulting API metadata payloads directly for terminal display.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.models.tvmaze_model import TVMazeModel
    from metatag.views.interactive import InteractiveWizard


class APIMetadataController:
    """Orchestrates interactive metadata menu flows using the TVMaze API wrapper."""

    def __init__(self, wizard: InteractiveWizard, tvmaze: TVMazeModel) -> None:
        """Initializes the presenter controller with the interactive wizard service."""
        self.wizard = wizard
        self.tvmaze = tvmaze

    def run(self) -> tuple[dict[str, Any], int, list[dict[str, Any]]]:
        """Runs the interactive selection pipeline and prints final filtered API data."""

        while True:
            print(f"{Theme.GREY}To cancel this prompt press ctrl+c{Theme.RESET}")

            # Step 1: Prompt for media type
            media_type = self.wizard.prompt_media_type()

            if media_type == "tv_series":
                # Step 2: Get show name from user
                show_name = self.wizard.prompt_show_name()

                # Step 3: Fuzzy search for TV Show name using TVMaze API
                raw_shows = self.tvmaze.fuzzy_search_show(show_name)

                # Guard Clause: Handle None or empty results safely!
                if not raw_shows:
                    print(f"{Theme.YELLOW}No shows found matching '{show_name}'. Please try again.{Theme.RESET}")
                    continue  # Restarts the search loop safely

                # Now the type checker knows 'raw_shows' is guaranteed to be a valid list[dict[str, Any]]
                # We can format the raw list into choice dictionaries for InquirerPy
                show_choices = []
                for show in raw_shows:
                    # Use fallback operators in case summary/status text is missing
                    status = show.get("status") or "Unknown Status"
                    premiered = show.get("premiered") or "TBA"

                    # Build a descriptive selection label for the user
                    label = f"{show['name']} ({premiered}) [{status}]"
                    show_choices.append({"name": label, "value": show})

                # Step 4: Display returned TV Shows from fuzzy search on TV_Maze
                selected_show = self.wizard.prompt_show_selection(show_choices)

                # Step 5: Display the seasons of the selected show
                show_id: int = selected_show["id"]

                seasons_choices = self.tvmaze.fetch_show_seasons(show_id)

                if not seasons_choices:
                    print(f"{Theme.YELLOW}No seasons found for this show. Please try again.{Theme.RESET}")
                    continue

                selected_season = self.wizard.prompt_season_selection(seasons_choices)

                # Step 6: Display the episodes of the selected season
                season_id = selected_season["id"]

                episode_choice = self.tvmaze.fetch_season_episodes_names(season_id)

                if not episode_choice:
                    print(f"{Theme.YELLOW}No episodes found for the {show_name} Season {season_id}")
                    continue

                manifest_names = [choice["name"] for choice in episode_choice]

                self.wizard.display_episode_manifest(manifest_names)

                # Step 6: Prompt to continue or exit, and capture the action
                next_action = self.wizard.prompt_continue_or_exit()

                if next_action == "restart":
                    print(f"\n{Theme.YELLOW}--- Restarting Wizard ---{Theme.RESET}\n")
                    self.wizard.clear_screen()
                    continue  # Jumps back to the top of the 'while True' loop

                # If they chose "continue", break out of the loop and return the data
                break

        return selected_show, season_id, manifest_names
