# pixel_kpi/processors/github/star_processor.py
from datetime import datetime
from typing import Dict, Tuple, List
from ..base_processor import BaseProcessor

class StarProcessor(BaseProcessor):
    """
    StarProcessor is responsible for processing the star data fetched from GitHub.
    It calculates the cumulative star count on a month-by-month basis.

    Attributes:
        DATE_FORMAT (str): The expected format for dates.
    """

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self) -> None:
        """Initializes the StarProcessor."""
        super().__init__()

    def extract_star_data(self, raw_data: Dict[str, int]) -> Tuple[List[str], List[int], str]:
        """
        Extracts star data for the current year, producing cumulative star counts for each month.

        Args:
            raw_data (Dict[str, int]): The raw data fetched from GitHub. Keys are date strings (YYYY-MM), 
                                       and values are the cumulative number of stars.

        Returns:
            Tuple[List[str], List[int], str]:
                - A list of month abbreviations (e.g., ["J", "F", "M"]).
                - A list of cumulative star counts for each month.
                - A formatted string representing the highest number of stars, abbreviated if greater than 1000.

        Raises:
            ValueError: If there are issues with the input data format.
        """
        current_year = datetime.now().year
        result = {}
        max_stars = 0

        # Initialize a dictionary with all months of the current year set to 0
        for month in range(1, 13):
            month_key = f"{current_year}-{month:02d}"
            result[month_key] = 0

        # Accumulate star data for the current year
        for date_str, star_count in raw_data.items():
            year, month = date_str.split('-')
            if int(year) == current_year:
                result[f"{year}-{month}"] = star_count
                if star_count > max_stars:
                    max_stars = star_count

        # Convert the data into a list format for easy rendering
        months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        stars = list(result.values())

        return months, stars, self._format_stars_str(max_stars)

    def _format_stars_str(self, stars: int) -> str:
        """
        Formats the star count as a string, abbreviating it if necessary.

        Args:
            stars (int): The number of stars.

        Returns:
            str: A string representing the number of stars. If greater than 1000, it is formatted as 'K'.
        """
        if stars >= 1000:
            return f"{stars // 1000}K"
        else:
            return str(stars)
