"""TVMaze API Model Component.

Manages data fetching, network request orchestration, and exception handling
for interacting with the TVMaze API endpoints.
"""

import time
from codecs import raw_unicode_escape_decode
from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


class TVMazeModel:
    """Handles data fetching specifically for the TVMaze API using httpx."""

    def __init__(self) -> None:
        self.base_url = "https://api.tvmaze.com"
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

    def fuzzy_search_show(self, show_name: str) -> list[dict[str, Any]] | None:
        """Queries TVMaze for show data and returns multiple shows information as a list."""
        search_url = f"{self.base_url}/search/shows"

        try:
            response = self._make_request(search_url, params={"q": show_name})

            # Specific Client-Side Route Actions
            if response.status_code == 404:
                return None

            # If any other unexpected 4xx error occurs (e.g., 400 Bad Request)
            response.raise_for_status()

            raw_results = response.json()

            fuzzy_shows_data = []

            for item in raw_results:
                if "show" in item:
                    fuzzy_shows_data.append(item["show"])

            return fuzzy_shows_data

        except httpx.HTTPStatusError as e:
            print(f"Client Error: {e.response.status_code} while quering TVMaze.")
            return None
        except httpx.HTTPError:
            print("Network Error: TVMaze API is completely unreachable right now.")
            return None

    def fetch_show_seasons(self, show_id: int) -> list[dict[str, Any]]:
        """Retrieves all seasons associated with a specific TV show ID.

        Queries the TVMaze '/shows/{id}/seasons' endpoint to collect the complete
        historical season log for the target asset.

        Args:
            show_id: The unique TVMaze database integer identifier for the show.

        Returns:
            A list of dictionaries, where each dictionary contains metadata for a single season.
        """
        seasons_url = f"{self.base_url}/shows/{show_id}/seasons"

        response = self._make_request(seasons_url)
        response.raise_for_status()

        raw_results = response.json()

        season_choices = []

        for season in raw_results:
            ep_order = season.get("episodeOrder")
            ep_count_str = f"{ep_order} episodes" if ep_order is not None else "TBA"

            label = f"Season {season['number']} ({ep_count_str})"

            season_choices.append({"name": label, "value": season})

        return season_choices

    def fetch_season_episodes_names(self, season_id: int) -> list[dict[str, Any]]:
        """Retrieves all episodes belonging to a specific season.

        Queries the TVMaze '/seasons/{id}/episodes' endpoint to collect the full
        list of episodes, including their metadata, for the designated season ID.

        Args:
            season_id: The unique TVMaze database integer identifier for the season.

        Returns:
            A list of dictionaries, where each dictionary contains the metadata profile
            of a single episode (e.g., name, episode number, runtime, airdate).

        Raises:
            httpx.HTTPStatusError: If the API returns an error status code.
            httpx.HTTPError: If a connection or network timeout occurs.
        """
        season_episodes = f"{self.base_url}/seasons/{season_id}/episodes"

        response = self._make_request(season_episodes)
        response.raise_for_status()

        raw_results = response.json()

        episode_choices = []

        for episode in raw_results:
            season_num = episode["season"]
            ep_num = episode.get("number")
            ep_name = episode.get("name") or "Untitled Episode"

            if ep_num is not None:
                marker = f"S{season_num:02d}E{ep_num:02d}"
            else:
                is_significant = episode.get("type") == "significant_special"
                marker = f"S{season_num:02d}-SPCL" if is_significant else f"S{season_num:02d}-SHORT"

            label = f"{marker} - {ep_name}"

            episode_choices.append({"name": label, "value": episode})

        return episode_choices
