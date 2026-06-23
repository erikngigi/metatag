"""API Metadata Information Presenter Controller.

Coordinates the data flow between the InteractiveWizard view/client engine
and formats the resulting API metadata payloads directly for terminal display.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from InquirerPy import inquirer

from metatag.views.theme import Theme, custom_style

if TYPE_CHECKING:
    from metatag.views.interactive import InteractiveWizard


class APIMetadataController:
    """Orchestrates interactive metadata menu flows using the TVMaze API wrapper."""

    def __init__(self, wizard: InteractiveWizard) -> None:
        """Initializes the presenter controller with the interactive wizard service."""
        self.wizard = wizard

    def run(self) -> tuple[dict, int, list]:
        """Runs the interactive selection pipeline and prints final filtered API data."""

        while True:
            print(f"{Theme.GREY}To cancel this prompt press ctrl+c{Theme.RESET}")

            # Step 1: Prompt for media type
            media_type = self.wizard.prompt_media_type()

            if media_type == "tv_series":
                # Step 2: Get show name from user
                show_name = self.wizard.prompt_show_name()

                # Step 3: Fetch show metadata and seasons bundle from the API
                show_data, seasons_data = self.wizard.fetch_show_metadata(show_name)

                if show_data["ended"] is None:
                    show_ended_status = "Ongoing"
                else:
                    show_ended_status = show_data["ended"]

                print(
                    f"{Theme.YELLOW}Show name: {show_data['name']}\n"
                    f"Status: {show_data['status']}\n"
                    f"Premiered On: {show_data['premiered']}\n"
                    f"Ended On: {show_ended_status}{Theme.RESET}"
                )

                # Re-map seasons data into clear choices dictionary keypairs for InquirerPy
                season_choices = []
                for season in seasons_data:
                    ep_count = season.get("episodeOrder") or "??"
                    label = f"Season {season['number']} ({ep_count} episodes)"
                    season_choices.append({"name": label, "value": season})

                # Prompt user to select a season using interactive arrows
                try:
                    selected_season = inquirer.select(
                        message="Select a season to inspect the episode list:",
                        choices=season_choices,
                        style=custom_style,
                    ).execute()
                except KeyboardInterrupt:
                    print(f"{Theme.RED}Operation cancelled.{Theme.RESET}")
                    sys.exit(0)

                # Extract the correct API sequence identifiers directly out of the selected choice value object
                chosen_season_num: int = selected_season["number"]
                season_id = selected_season["id"]

                # Step 4: Fetch episodes exclusively for that season ID
                episodes = self.wizard.fetch_season_episodes(season_id)

                # Step 5: Render final episode names from the API payload
                print(f"{show_data['name']} - Season {chosen_season_num} episode list:")
                for ep in episodes:
                    ep_num = ep.get("number")
                    ep_str = f"{ep_num:02d}" if ep_num is not None else "??"
                    print(f"{ep_str} - {ep['name']}")
                print()

                # Step 6: Prompt to continue or exit, and capture the action
                next_action = self.wizard.prompt_continue_or_exit()

                if next_action == "restart":
                    print(f"\n{Theme.YELLOW}--- Restarting Wizard ---{Theme.RESET}\n")
                    self.wizard.clear_screen()
                    continue  # Jumps back to the top of the 'while True' loop

                # If they chose "continue", break out of the loop and return the data
                break

        return show_data, chosen_season_num, episodes
