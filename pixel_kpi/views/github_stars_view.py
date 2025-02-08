# pixel_kpi/views/github_stars_view.py
from ..displays.base_display import BaseDisplay
from .base_view import BaseView
from ..components.text import Text
from ..components.bar_chart import BarChart
from ..components.headline import Headline
from ..connectors.github_connector import GithubConnector
from ..processors.github.star_processor import StarProcessor
from typing import Dict, Tuple

class GithubStarsView(BaseView):
    """
    GithubStarsView displays GitHub repository star data on a Pixoo display.
    
    Attributes:
        repository (str): The GitHub repository to track stars (in 'owner/repo' format).
    """

    def __init__(self, display: BaseDisplay, connector: GithubConnector, processor: StarProcessor, main_color: Tuple[int, int, int], refresh_rate: int = 60*15, repository: str = "pi_optimal/pi_optimal") -> None:
        """
        Initializes the GithubStarsView with the specified display, connector, processor, and repository.

        Args:
            display (BaseDisplay): The display to render the star data on.
            connector (GithubConnector): The GitHub connector to fetch star data.
            processor (StarProcessor): The processor to handle GitHub star data.
            main_color (Tuple[int, int, int]): The main color for rendering.
            refresh_rate (int): The refresh rate for updating the display.
            repository (str): The GitHub repository in 'owner/repo' format.
        """
        super().__init__(display, connector, processor, refresh_rate, main_color)
        self.repository = repository

    def _get_stars_data(self) -> Dict[str, any]:
        """
        Fetches and processes the star data for the repository.

        Returns:
            Dict[str, any]: Contains the months, stars, and max stars for the repository.
        """
        stars_data_raw = self.connector.download_stargazers(repository=self.repository)
        months, stars, max_stars = self.processor.extract_star_data(stars_data_raw)

        return {"months": months, "stars": stars, "max_stars": max_stars}

    def draw_view(self, sprint_data: Dict[str, any]) -> None:
        """
        Draws the GitHub stars view on the display.

        Args:
            sprint_data (Dict[str, any]): The processed star data.
        """
        self.display.clear()
        Text.draw(self.display, text="Stars", position=(36, 5), color=self.main_color)
        Text.draw(self.display, text="Github", position=(36, 10), color=self.main_color)
        Headline.draw(self.display, text=str(sprint_data["max_stars"]), position=(2, 5), scale=2, color=self.main_color)
        Text.draw(self.display, text="Repo:", position=(2, 18), color=self.main_color)
        Text.draw(self.display, text=self.repository.split("/")[1], position=(2, 24), color=self.main_color)
        BarChart.draw(self.display, data=sprint_data["stars"], labels=sprint_data["months"], position=(2, 33), max_height=20, bar_width=3, spacing=2, color=self.main_color)

    def refresh(self) -> None:
        """
        Refreshes the GitHub stars view with updated star data.
        """
        stars_data = self._get_stars_data()
        self.logger.info(f"Refreshing view with star data: {stars_data}")
        self.display.clear()
        self.draw_view(stars_data)
        self.display.render()
