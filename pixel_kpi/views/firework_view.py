# pixel_kpi/views/github_stars_view.py
from ..displays.base_display import BaseDisplay
from .base_view import BaseView
from ..components.firework import Firework
from ..components.text import Text
from typing import Dict
import time

class FireworkView(BaseView):
    """
    FireworkView displays a firework animation on the display.
    
    """

    def __init__(self, display: BaseDisplay, headline: str, subheadline: str, refresh_rate: int = 60*15) -> None:
        """
        Initializes the FireworkView with the specified display and main color.

        Args:
            display (BaseDisplay): The display to render the star data on.
            headline (str): The headline for the firework animation.
            subheadline (str): The subheadline for the firework animation.
            refresh_rate (int): The refresh rate for updating the display.
        """
        super().__init__(display, None, None, refresh_rate, None)
        self.headline = headline
        self.subheadline = subheadline


    def refresh(self) -> None:
        """
        Refreshes the firework animation on the display.
        """

        self.logger.info(f"Refreshing FireworkView")


        self.display.clear()

        firework_1 = Firework(display=self.display, max_height=50, position=(64, 32))
        firework_2 = Firework(display=self.display, max_height=30, position=(64, 15))
        firework_3 = Firework(display=self.display, max_height=47, position=(64, 20))
        firework_4 = Firework(display=self.display, max_height=50, position=(64, 23))
        firework_5 = Firework(display=self.display, max_height=53, position=(64, 56))

        while True:
            for i in range(200):
                
                Text.draw(self.display, text=self.headline, position=(18, 20), color=(255, 255, 255))
                Text.draw(self.display, text=self.subheadline, position=(14, 30), color=(255, 255, 255))

                if i > 2:
                    firework_1.draw()
                if i > 40:
                    firework_2.draw()
                if i > 60:
                    firework_3.draw()
                if i > 90:
                    firework_4.draw()
                if i > 100:
                    firework_5.draw()
                time.sleep(0.05)
                self.display.render()
