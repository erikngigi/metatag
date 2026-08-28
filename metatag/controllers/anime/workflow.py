"""Anime Metadata Selector Controller for testing search capabilities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.colors import colors, cprint
from metatag.controllers.anime.renamer import AnimeRenamerController
from metatag.controllers.shared.directory_selector import DirectoryController
from metatag.controllers.shared.file_selector import FileSelectorController

if TYPE_CHECKING:
    from metatag.models.anime_model import AnimeTenraiModel
    from metatag.views.anime_menu import AnimeMenuView
    from metatag.views.base_menu import BaseMenuView


class AnimeSelectorController:
    """Manages the standalone selection pipeline specifically for Anime series using Jikan API."""

    def __init__(
        self,
        anime_menu: AnimeMenuView,
        base_menu: BaseMenuView,
        anime_tenrai: AnimeTenraiModel,
    ) -> None:
        self.anime_menu = anime_menu
        self.base_menu = base_menu
        self.tenrai = anime_tenrai

    def execute(self, args: Any) -> None:
        """Executes a single-run check of the Anime search and selection filters."""
        while True:
            # Step 1: Get anime details from the user via unified prompt filters
            anime_detail_filters = self.anime_menu.prompt_anime_search_filters()

            # Step 2: Fuzzy search using the Tenrai API Model wrapper
            fuzzy_search_anime = self.tenrai.fuzzy_search_anime(
                anime_name=anime_detail_filters.anime_name,
                anime_type=anime_detail_filters.anime_type,
                anime_status=anime_detail_filters.anime_status,
            )

            if not fuzzy_search_anime or not fuzzy_search_anime.data:
                cprint(colors.YELLOW, f"No anime found matching '{anime_detail_filters.anime_name}'.")
                continue

            # Step 3: Format choices and prompt for direct list selection
            anime_choices = []
            for anime in fuzzy_search_anime.data:
                anime_choices.append({"name": anime.summary_label, "value": anime})

            # Step 4: User picks the anime from the search result choices
            selected_anime = self.anime_menu.prompt_anime_selection(anime_choices)

            # Step 5: Make an initial lightweight call to fetch page 1 to inspect the pagination limits
            initial_payload = self.tenrai.fetch_anime_episodes_names(selected_anime.id, page=1)

            while True:
                if not initial_payload:
                    cprint(colors.YELLOW, "No episodes found or could not fetch manifest for this anime.")
                    continue

                # Unpack the initial data, capturing the exact total number of pages
                initial_episodes, total_pages = initial_payload

                # Step 6: Determine page configuration and prompt the user BEFORE building the manifest names
                chosen_page = 1
                if total_pages > 1:
                    # Call your wizard method to let the user select their page index upfront
                    chosen_page = self.anime_menu.prompt_anime_page_selection(max_pages=total_pages)

                # Step 7: Perform a final targeted API request ONLY if they chose a page other than Page 1
                if chosen_page == 1:
                    target_episode_list = initial_episodes
                else:
                    final_payload = self.tenrai.fetch_anime_episodes_names(selected_anime.id, page=chosen_page)

                    if not final_payload:
                        cprint(colors.YELLOW, f"Could not retrieve metadata for page {chosen_page}.")
                        continue

                    target_episode_list, _ = final_payload

                # Step 8: Process and format the list using the chosen page context offset
                selected_anime_episode_names: list[str] = []

                # Tenrai returns 100 items per page.
                # Page 1 starts at index 1. Page 2 starts at ((2-1)*100)+1 = 101.
                start_index = ((chosen_page - 1) * 100) + 1

                for index, episode in enumerate(target_episode_list, start=start_index):
                    # Using 1-based continuous absolute indexing typical for anime naming conventions
                    label = f"{selected_anime.title_english} {index:02d} - {episode.title}"
                    selected_anime_episode_names.append(label)

                # self.base_menu.print_episodes(selected_anime_episode_names)
                self.anime_menu.print_anime_episode_manifest(selected_anime.title, selected_anime_episode_names)

                # Step 9: Loop control
                next_action = self.anime_menu.prompt_anime_post_checkpoint()

                if next_action == "rename":
                    selected_episode_manifest = self.base_menu.prompt_episode_selection(selected_anime_episode_names)

                    if not selected_episode_manifest:
                        cprint(colors.YELLOW, "No remote episodes selected. Aborting rename phase.")
                        continue

                    dir_controller = DirectoryController(self.base_menu)
                    target_dir = dir_controller.run(media_type="anime_series")

                    file_controller = FileSelectorController(self.base_menu, target_dir)
                    files_to_process = file_controller.run()

                    anime_renamer = AnimeRenamerController(
                        target_dir=target_dir, local_files=files_to_process, episode_manifest=selected_episode_manifest
                    )

                    if files_to_process:
                        # Explicit --dry-run flag: preview only, no confirmation needed
                        if getattr(args, "preview", False):
                            anime_renamer.rename_anime_episodes(anime_name=selected_anime.title_english, preview=True)
                        else:
                            anime_renamer.rename_anime_episodes(anime_name=selected_anime.title_english, preview=True)

                            proceed = self.base_menu.prompt_confirmation(
                                message="Do you want to proceed with renaming these files?",
                                default=False,
                            )

                            if not proceed:
                                cprint(colors.YELLOW, "Renaming sequence aborted by user. No files were changed.")
                                return

                            anime_renamer.rename_anime_episodes(
                                anime_name=selected_anime.title_english, preview=args.preview
                            )
                        return

                elif next_action == "alternate_page":
                    self.base_menu.clear_screen()
                    cprint(colors.CYAN, f"Reloading {selected_anime.title_english} seasons list.")
                    continue

                elif next_action == "search_again":
                    self.base_menu.clear_screen()
                    break
