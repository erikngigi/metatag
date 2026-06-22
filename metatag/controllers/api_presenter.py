"""API Metadata Information Presenter Controller.

Coordinates the data flow between the InteractiveWizard view/client engine
and formats the resulting API metadata payloads directly for terminal display.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from InquirerPy import inquirer

# from InquirerPy.utils import InquirerPyStyle

if TYPE_CHECKING:
    from metatag.views.interactive import InteractiveWizard

# Import identical theme styling for visual uniformity across menus
from metatag.views.interactive import custom_style

cyan = "\033[36m"
bold = "\033[1m"
reset = "\033[0m"


class APIMetadataController:
    """Orchestrates interactive metadata menu flows using the TVMaze API wrapper."""

    def __init__(self, wizard: InteractiveWizard) -> None:
        """Initializes the presenter controller with the interactive wizard service."""
        self.wizard = wizard

    def run(self) -> None:
        """Runs the interactive selection pipeline and prints final filtered API data."""
        print("\033[90mTo cancel this prompt press ctrl+c / ctrl+z\033[0m\n")

        # Step 1: Prompt for media type
        media_type = self.wizard.prompt_media_type()

        if media_type == "tv":
            # Step 2: Get show name from user
            show_name = self.wizard.prompt_show_name()

            # Step 3: Fetch show metadata and seasons bundle from the API
            show_data, seasons_data = self.wizard.fetch_show_metadata(show_name)

            print(f"\nMatched: {show_data['name']} ({show_data.get('language', 'Unknown')})")

            # Re-map seasons data into clear choices dictionary keypairs for InquirerPy
            season_choices = []
            for season in seasons_data:
                ep_count = season.get("episodeOrder") or "??"
                label = f"Season {season['number']} ({ep_count} episodes)"
                season_choices.append({"name": label, "value": season})

            # Prompt user to select a season using interactive arrows
            try:
                selected_season = inquirer.select(
                    message="Select a season to inspect:", choices=season_choices, style=custom_style
                ).execute()
            except KeyboardInterrupt:
                print("\n\n\033[91m[!] Operation cancelled. Exiting safely...\033[0m")
                sys.exit(0)

            # Extract the correct API sequence identifiers directly out of the selected choice value object
            chosen_season_num = selected_season["number"]
            season_id = selected_season["id"]

            # Step 4: Fetch episodes exclusively for that season ID
            episodes = self.wizard.fetch_season_episodes(season_id)

            # Step 5: Render final episode names from the API payload
            # print(f"\n{show_data['name']} - Season {chosen_season_num} Episode List")
            # for ep in episodes:
            #     # print(f" S{ep['season']:02d}E{ep['number']:02d} - {ep['name']}")
            #     print(f" E{ep['number']:02d} - {ep['name']}")
            # # print("====================================================\n")
            # print("\n")

            # Step 5: Render final episode names from the API payload
            print(f"\n{bold}{cyan}{show_data['name']}{reset} - Season {chosen_season_num} Episode List")
            for ep in episodes:
                # Check if the number exists, otherwise format it as a fallback string placeholder
                ep_num = ep.get("number")
                ep_str = f"{ep_num:02d}" if ep_num is not None else "??"

                print(f"{ep_str} - {ep['name']}")
            # print("\n")
