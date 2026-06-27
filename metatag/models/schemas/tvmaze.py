"""TVMaze API Data Validation and Serialization Schemas.

Provides Pydantic schemas to validate and sanitize incoming JSON payloads
from TVMaze endpoints, preventing structural key errors and enforcing strict
type safety before data flows down to application controllers.

Exported Schemas:
    TVShowSchema: Validates show metadata and calculates broadcast year ranges.
    TVSeasonSchema: Validates season metrics and builds summary labels.
    TVEpisodeSchema: Validates individual episode data and generates naming tokens.
"""

from typing import Optional

from pydantic import BaseModel, Field


class TVShowSchema(BaseModel):
    """Pydantic schema representing a validated TV show entity from the TVMaze API.

    This schema enforces structural integrity and handles data validation for top-level
    series properties returned from fuzzy search endpoints, shielding controllers
    from raw dictionary lookups.

    Attributes:
        id (int): Unique database identifier assigned by TVMaze.
        name (str): Official, primary title of the television series.
        language (Optional[str]): Primary spoken language of the show (defaults to "Unknown").
        status (str): Current production status of the series (e.g., "Running", "Ended").
        premiered (Optional[str]): ISO 8601 formatted premiere date string (YYYY-MM-DD) or None.
        ended (Optional[str]): ISO 8601 formatted series finale date string (YYYY-MM-DD) or None.

    Properties:
        year_range (str): Computes a human-readable representation of the show's broadcast span.

    Raises:
        pydantic.ValidationError: If the payload contains invalid data types or lacks mandatory fields.
    """

    id: int
    name: str
    language: Optional[str] = "Unknown"
    status: str
    premiered: Optional[str] = None
    ended: Optional[str] = None

    @property
    def year_range(self) -> str:
        """Derived property logic wrapped safely within the schema data boundary."""
        start_year = self.premiered.split("-")[0] if self.premiered else "TBA"
        if self.status.lower() == "running":
            return f"{start_year} - Present"
        end_year = self.ended.split("-")[0] if self.ended else "TBA"
        return f"{start_year} - {end_year}"


class TVSeasonSchema(BaseModel):
    """Pydantic schema representing a tracking segment for a specific TV show season.

    This schema validates structural metrics for a specific season block, providing
    clean formatting methods to standardise data for interactive terminal selection menus.

    Attributes:
        id (int): Unique database identifier assigned by TVMaze for the season.
        number (int): Numerical sequence order of the season within the series run.
        episodeOrder (Optional[int]): Total number of scheduled episodes in this season track.
        premiereDate (Optional[str]): ISO 8601 formatted release date of the season's first episode.
        endDate (Optional[str]): ISO 8601 formatted release date of the season's final episode.

    Properties:
        summary_label (str): Generates a formatted descriptive string for terminal user interfaces.

    Raises:
        pydantic.ValidationError: If payload types break integer parsing rules or lack identifier keys.
    """

    id: int
    number: int
    episodeOrder: Optional[int] = None
    premiereDate: Optional[str] = None
    endDate: Optional[str] = None

    @property
    def summary_label(self) -> str:
        """Generates the clean UI text string out of validated properties."""
        ep_count_str = f"{self.episodeOrder} episodes" if self.episodeOrder is not None else "TBA"
        start_year = self.premiereDate.split("-")[0] if self.premiereDate else "TBA"
        end_year = self.endDate.split("-")[0] if self.endDate else "TBA"
        return f"Season {self.number} ({ep_count_str})  ({start_year} - {end_year})"


class TVEpisodeSchema(BaseModel):
    """Pydantic schema representing an individual episode manifest entry.

    This schema isolates structural data for individual episodes, protecting file
    handling pipelines from missing naming attributes and facilitating safe token generation.

    Attributes:
        season (int): Numerical sequence order of the parent season.
        number (Optional[int]): Numerical sequence order of the episode within its season.
        name (str): Title label of the episode (defaults to "Untitled Episode").
        type (str): Categorization flag of the track (e.g., "regular", "significant_special").

    Properties:
        marker (str): Derives a standard token (e.g., SxxExx or Sxx-SPCL) for automatic file renaming.

    Raises:
        pydantic.ValidationError: If structural tracking bounds or mandatory integer data are invalid.
    """

    season: int
    number: Optional[int] = None
    name: str = Field(default="Untitled Episode")
    type: str = "regular"

    @property
    def marker(self) -> str:
        """Derives the SxxExx tracking token cleanly."""
        if self.number is not None:
            return f"S{self.season:02d}E{self.number:02d}"
        is_significant = self.type == "significant_special"
        return f"S{self.season:02d}-SPCL" if is_significant else f"S{self.season:02d}-SHORT"
