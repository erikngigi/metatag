"""Anime Metadata Selector Controller for testing search capabilities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from metatag.views.theme import Theme

if TYPE_CHECKING:
    from metatag.models.anime_model import AnimeJikanModel
    from metatag.models.schemas.anime import AnimeDetailsSchema
    from metatag.views.interactive import InteractiveWizard


class AnimeSelectorController:
    """Manages the standalone selection pipeline specifically for Anime series using Jikan API."""

    def __init__(self, wizard: InteractiveWizard, anime: AnimeJikanModel) -> None:
        self.wizard = wizard
        self.jikan = anime

    def execute(self, args: Any) -> None:
        """Executes a single-run check of the Anime search and selection filters."""
        # Step 1: Get anime details from the user via unified prompt filters
        anime_detail_filters = self.wizard.prompt_anime_search_filters()

        # Step 2: Fuzzy search using the Jikan API Model wrapper
        fuzzy_search_anime = self.jikan.fuzzy_search_anime(
            anime_name=anime_detail_filters.anime_name,
            anime_type=anime_detail_filters.anime_type,
            anime_status=anime_detail_filters.anime_status,
        )

        if not fuzzy_search_anime or not fuzzy_search_anime.data:
            print(f"{Theme.YELLOW}No anime found matching '{anime_detail_filters.anime_name}'.{Theme.RESET}")
            return

        # Step 3: Format choices and prompt for direct list selection
        anime_choices = []
        for anime in fuzzy_search_anime.data:
            anime_choices.append({"name": anime.summary_label, "value": anime})

        # Step 1: User picks the anime from the search result choices
        selected_anime: AnimeDetailsSchema = self.wizard.prompt_anime_selection(anime_choices)

        # Step 2: Make an initial lightweight call to fetch page 1 to inspect the pagination limits
        initial_payload = self.jikan.fetch_anime_episodes_names(selected_anime.id, page=1)

        if not initial_payload:
            print(f"{Theme.YELLOW}No episodes found or could not fetch manifest for this anime.{Theme.RESET}")
            return None

        # Unpack the initial data, capturing the exact total number of pages
        initial_episodes, total_pages = initial_payload

        # Step 3: Determine page configuration and prompt the user BEFORE building the manifest names
        chosen_page = 1
        if total_pages > 1:
            # Call your wizard method to let the user select their page index upfront
            chosen_page = self.wizard.prompt_anime_page_selection(max_pages=total_pages)

        # Step 4: Perform a final targeted API request ONLY if they chose a page other than Page 1
        if chosen_page == 1:
            target_episode_list = initial_episodes
        else:
            final_payload = self.jikan.fetch_anime_episodes_names(selected_anime.id, page=chosen_page)
            if not final_payload:
                print(f"{Theme.YELLOW}Could not retrieve metadata for page {chosen_page}.{Theme.RESET}")
                return None
            target_episode_list, _ = final_payload

        # Step 5: Process and format the list using the chosen page context offset
        selected_anime_episode_names: list[str] = []

        # Jikan returns 100 items per page.
        # Page 1 starts at index 1. Page 2 starts at ((2-1)*100)+1 = 101.
        start_index = ((chosen_page - 1) * 100) + 1

        for index, episode in enumerate(target_episode_list, start=start_index):
            # Using 1-based continuous absolute indexing typical for anime naming conventions
            label = f"Episode {index:02d} - {episode.title}"
            selected_anime_episode_names.append(label)

        self.wizard.display_episode_manifest(selected_anime_episode_names)
