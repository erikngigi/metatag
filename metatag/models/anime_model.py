"""Jikan Anime API Model Component.

Manages data fetching, network request orchestration, and exception handling
for interacting with the Jikan Anime API endpoints.
"""

import time
from typing import Any, Optional

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from metatag.models.schemas import anime
from metatag.models.schemas.anime import AnimeEpisodeResponse, AnimeEpisodeSchema, AnimeSearchResponse


class AnimeTenraiModel:
    """Handles data fetching specifically for the Tenrai Anime API using httpx."""

    def __init__(self) -> None:
        self.base_url = "https://api.tenrai.org/v1"
        # Using an HTTPX client handles connection pooling efficiently
        self.client = httpx.Client(timeout=10.0)

    # Automatically retry on network timeouts or server-side errors (5xx/429)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError)),
        reraise=True,
    )
    def _make_request(self, url: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """Internal helper to enforce request rules and catch errors."""
        response = self.client.get(url, params=params)

        # If status code is 429 (Rate Limited) or 5xx (Server Error), raise an exception to trigger a retry
        if response.status_code == 429 or response.status_code >= 500:
            response.raise_for_status()

        return response

    def fuzzy_search_anime(
        self,
        anime_name: str,
        anime_type: Optional[str] = None,
        anime_status: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
    ) -> Optional[AnimeSearchResponse]:
        """Queries Tenrai for show data and returns multiple shows information as a list."""
        search_url = f"{self.base_url}/anime"

        # 1. Build initial params dictionary
        raw_params = {"q": anime_name, "type": anime_type, "status": anime_status, "page": page, "limit": limit}

        params = {k: v for k, v in raw_params.items() if v is not None}

        aggregated_animes = []
        current_page = page
        has_next = True
        final_pagination = None

        try:
            while has_next:
                params["page"] = current_page
                response = self._make_request(search_url, params=params)

                # Specific Client-Side Route Actions
                if response.status_code == 404:
                    break

                # If any other unexpected 4xx error occurs (e.g., 400 Bad Request)
                response.raise_for_status()
                raw_payload = response.json()

                page_response = AnimeSearchResponse.model_validate(raw_payload)

                if page_response.data:
                    aggregated_animes.extend(page_response.data)

                final_pagination = page_response.pagination
                has_next = final_pagination.has_next_page

                if has_next:
                    current_page += 1
                    time.sleep(1.0)

            if not final_pagination:
                return None

            return AnimeSearchResponse(pagination=final_pagination, data=aggregated_animes)

        except httpx.HTTPStatusError as e:
            print(f"Client Error: {e.response.status_code} while quering Tenrai Anime API.")
            return None
        except httpx.HTTPError:
            print("Network Error: Tenrai Anime API is completely unreachable right now.")
            return None

    def fetch_anime_episodes_names(
        self, anime_mal_id: int, page: int = 1
    ) -> Optional[tuple[list[AnimeEpisodeSchema], int]]:
        """Retrieves all episodes belonging to a specific Anime.

        Queries the Tenrai '/anime/{anime_mal_id}/episodes' endpoint to collect the full
        list of episodes, including their metadata, for the designated season ID.

        Args:
            anime_mal_id: The unique Mal ID database integer identifier for the anime.

        Returns:
            A list of dictionaries, where each dictionary contains the metadata profile
            of a single episode (e.g., mal_id, title, aired, score, filler and recap).

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.HTTPError: If a connection or network timeout occurs.
        """
        anime_episodes_url = f"{self.base_url}/anime/{anime_mal_id}/episodes"

        params = {"page": page}

        try:
            response = self._make_request(anime_episodes_url, params=params)

            if response.status_code == 404:
                return None

            response.raise_for_status()
            raw_payload = response.json()

            page_response = AnimeEpisodeResponse.model_validate(raw_payload)

            return page_response.data, page_response.pagination.last_visible_page

        except httpx.HTTPStatusError as e:
            print(f"Client Error: {e.response.status_code} while querying Tenrai Anime API endpoint for episodes.")
            return None
        except httpx.HTTPError:
            print("Network Error: Tenrai Anime API is completely unreachable right now.")
            return None
