# pixel_kpi/views/github_stars_view.py
from ..displays.base_display import BaseDisplay
from .base_view import BaseView
from ..components.text import Text
from ..components.bar_chart import BarChart
from ..components.headline import Headline
from typing import Dict, Tuple
from ..connectors.pypi_connector import PyPiConnector   


class PackageDownloadView(BaseView):
    """
    PackageDownloadView displays the download count of a package.
    """

    def __init__(self, display: BaseDisplay, connector: PyPiConnector, processor: None, main_color: Tuple[int, int, int], refresh_rate: int = 60*15, package_name: str = "pi_optimal") -> None:
        """
        Initializes the PiOptimalView with the specified display, connector, processor, and repository.

        Args:
            display (BaseDisplay): The display to render the star data on.
            connector (PyPiConnector): The Plausible connector to fetch star data.
            processor (StarProcessor): The processor to handle GitHub star data.
            main_color (Tuple[int, int, int]): The main color for rendering.
            refresh_rate (int): The refresh rate for updating the display.
            repository (str): The GitHub repository in 'owner/repo' format.
        """
        super().__init__(display, connector, processor, refresh_rate, main_color)
        self.package_name = package_name

    def _get_package_downloads(self) -> int:
        """
        Fetches the download count of the package.

        Returns:
            int: The download count of the package.
        """
        views = self.connector.get_downloads(self.package_name)

        return views

    def draw_view(self, display_data: Dict[str, any]) -> None:
        """
        Draws the pi_optimal view on the display.

        Args:
            sprint_data (Dict[str, any]): The processed star data.
        """

        self.display.clear()
        
        #Headline.draw(self.display, text="Package: " + self.package_name, position=(0, 0), scale=1, color=self.main_color)
        Text.draw(self.display, text="Downloads: " + str(display_data["package_downloads"]), position=(2, 10), color=self.main_color)


    def refresh(self) -> None:
        """
        Refreshes the GitHub stars view with updated star data.
        """
      
        package_downloads = self._get_package_downloads()
        display_data = {"package_downloads": package_downloads}
        self.logger.info(f"Refreshing view with current data: {display_data}")
        self.display.clear()
        self.draw_view(display_data)
        self.display.render()
