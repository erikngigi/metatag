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

        # Prompts selection grid
        selected_anime: AnimeDetailsSchema = self.wizard.prompt_anime_selection(anime_choices)

        selected_anime_episode_list, pagination = self.jikan.fetch_anime_episodes_names(selected_anime.id)

        if not selected_anime_episode_list:
            print(f"{Theme.YELLOW}No episodes found or could not fetch manifest for this anime.{Theme.RESET}")
            return None

        selected_anime_episode_names: list[str] = []
        for index, episode in enumerate(selected_anime_episode_list, start=1):
            # Using 1-based continuous absolute indexing typical for anime naming conventions
            label = f"Episode {index:02d} - {episode.title}"
            selected_anime_episode_names.append(label)

        self.wizard.display_episode_manifest(selected_anime_episode_names)
