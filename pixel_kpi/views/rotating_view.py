# pixel_kpi/views/rotating_view.py
from ..displays.base_display import BaseDisplay
import time
from .base_view import BaseView
from typing import List

class RotatingView(BaseView):
    """
    RotatingView is responsible for rotating between multiple views on a display.
    
    Attributes:
        views (List[BaseView]): A list of views to rotate between.
        switch_interval (int): Time (in seconds) between view switches.
        current_view_index (int): The index of the currently active view.
        running (bool): Whether the rotation loop is running.
    """

    def __init__(self, display: BaseDisplay, views: List[BaseView], switch_interval: int = 60, refresh_rate: int = 60*15) -> None:
        """
        Initializes the RotatingView with a list of views and a switch interval.

        Args:
            display (BaseDisplay): The display to render the rotating views on.
            views (List[BaseView]): A list of views to rotate between.
            switch_interval (int): Time interval (in seconds) between view switches.
            refresh_rate (int): The refresh rate for updating the display.
        """
        super().__init__(display, None, None, refresh_rate, None)
        self.views = views
        self.switch_interval = switch_interval
        self.current_view_index = 0
        self.running = False

    def run(self) -> None:
        """
        Handles the logic to switch between views in a loop.
        """
        while True:
            current_view = self.views[self.current_view_index]
            current_view.refresh()  # Refreshes the current view
            time.sleep(self.switch_interval)  # Waits for the specified interval
            self.current_view_index = (self.current_view_index + 1) % len(self.views)  # Switch to the next view
