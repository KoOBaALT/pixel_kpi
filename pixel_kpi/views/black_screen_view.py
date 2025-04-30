# pixel_kpi/views/github_stars_view.py
from ..displays.base_display import BaseDisplay
from .base_view import BaseView
from typing import Tuple
import time

class BlackScreenView(BaseView):
    """
    FireworkView displays a firework animation on the display.
    
    """

    def __init__(self, display: BaseDisplay, refresh_rate: int = 60*15, main_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Initializes the FireworkView with the specified display and main color.

        Args:
            display (BaseDisplay): The display to render the star data on.
            headline (str): The headline for the firework animation.
            subheadline (str): The subheadline for the firework animation.
            refresh_rate (int): The refresh rate for updating the display.
        """
        super().__init__(display, None, None, refresh_rate, main_color)

    def refresh(self) -> None:
        """
        Refreshes the firework animation on the display.
        """

        self.logger.info(f"Refreshing FireworkView")

        self.display.clear()
        self.display.render()
