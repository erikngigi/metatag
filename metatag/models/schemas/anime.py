"""
Pydantic data models for API response validation and data parsing.

This module provides structured data schemas for handling and validating media metadata
ingested from downstream external anime API (Tenrai API) for micro-services across CLI
wizard controller routers.
"""

from typing import Optional

from pydantic import BaseModel, Field


class AnimeSearchQuery(BaseModel):
    """Data schema representing a structured search query for the Tenrai Anime API.

    This Pydantic model validates and encapsulates raw interactive wizard user inputs
    governing targeted name criteria, format variations, and tracking status states
    prior to endpoint dispatching.

    Attributes:
        anime_name: The raw search string or title term provided by the user.
        anime_type: Filter specifying the layout format (e.g., 'tv', 'movie', 'ova').
        anime_status: Filter targeting current airing lifecycle state (e.g., 'complete', 'airing').
    """

    anime_name: str
    anime_type: str
    anime_status: str


class PaginationItems(BaseModel):
    """Represents the volume and layout metrics of data items on a single page."""

    count: int
    total: int
    per_page: int


class PaginationSearch(BaseModel):
    """A unified pagination search model that handles both detailed and minimal API responses."""

    last_visible_page: int
    has_next_page: bool
    current_page: Optional[int]
    items: Optional[PaginationItems]


class PaginationEpisodes(BaseModel):
    """A unified pagination episode model that handles both detailed and minimal API responses."""

    last_visible_page: int
    has_next_page: bool


class AnimeDetailsSchema(BaseModel):
    """Data schema representing validated anime series metadata from the Tenrai API.

    This Pydantic model acts as a structural validation layer for handling raw, JSON-parsed
    payload responses returned by downstream Tenrai search endpoints. It sanitizes data,
    handles alias mappings, and exposes properties for user-facing CLI presentation loops.

    Attributes:
        id (int): Unique database identifier assigned by MyAnimeList, aliased from 'mal_id'.
        title (str): Canonical main title of the anime asset.
        title_english (Optional[str]): Official English localization title, if available.
        title_japanese (Optional[str]): Native Japanese title name.
        type (Optional[str]): Release presentation format (e.g., 'TV', 'Movie', 'OVA', 'Special').
        source (Optional[str]): Original source medium material origin (e.g., 'Manga', 'Light Novel').
        episodes (Optional[int]): Total broadcast or production episode count.
        status (str): Current publishing/airing production lifecycle state (e.g., 'Finished Airing').
        airing (bool): Flag indicating if the series is currently broadcasting.
        year (Optional[int]): Premier broadcast calendar year.
        season (Optional[str]): Premier calendar release season climate group (e.g., 'spring', 'fall').
    """

    id: int = Field(..., alias="mal_id")
    title: str
    title_english: Optional[str] = None
    title_japanese: Optional[str] = None
    type: Optional[str] = None
    source: Optional[str] = None
    episodes: Optional[int] = None
    status: str
    airing: bool
    year: Optional[int] = None
    season: Optional[str] = None

    class Config:
        populate_by_name = True  # Allows parsing raw payload mapping via 'mal_id'

    @property
    def summary_label(self) -> str:
        """Generates a standardized display string for your InquirerPy options loop."""
        display_title = self.title_english if self.title_english else self.title
        ep_count = f"{self.episodes} eps" if self.episodes else "Unknown eps"
        year_str = f" ({self.year})" if self.year else ""

        return f"󰎁 {display_title}{year_str}   [{self.type}]   {ep_count} ({self.status})"


class AnimeEpisodeSchema(BaseModel):
    """Pydantic schema representing an individual anime episode manifest entry.

    This schema isolates structural data for individual anime episodes ingested from
    downstream Tenrai API endpoints, shielding file-handling pipelines from missing naming
    attributes and facilitating absolute-number token generation for renaming structures.

    Attributes:
        id (int): Unique database identifier assigned by MyAnimeList, aliased from 'mal_id'.
        title (str): Canonical localized title name of the individual episode.
        aired (Optional[str]): ISO 8601 formatted broadcast release date string or None.
        score (Optional[float]): Community rating score metric assigned to the entry.
        is_filler (bool): Flag indicating if the episode is classified as non-canon filler material,
            aliased from 'filler'.
        is_recap (bool): Flag indicating if the track layout serves as a production summary block,
            aliased from 'recap'.

    Raises:
        pydantic.ValidationError: If payload validation types break structural baseline
            bounds or lack mandatory tracking keys.
    """

    id: int = Field(..., alias="mal_id")
    title: str
    aired: Optional[str] = None
    score: Optional[float] = None
    is_filler: bool = Field(..., alias="filler")
    is_recap: bool = Field(..., alias="recap")

    class Config:
        populate_by_name = True


class AnimeSearchResponse(BaseModel):
    """The complete top-level envelope structure of the API response."""

    pagination: PaginationSearch
    data: list[AnimeDetailsSchema]


class AnimeEpisodeResponse(BaseModel):
    """The complete top-level envelope structure of the API response."""

    pagination: PaginationEpisodes
    data: list[AnimeEpisodeSchema]
