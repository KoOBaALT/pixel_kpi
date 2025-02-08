# pixel_kpi/views/base_view.py
import logging
from ..displays.base_display import BaseDisplay
from ..connectors.base_connector import BaseConnector
from ..processors.base_processor import BaseProcessor
import time
from typing import Optional, Tuple

class BaseView:
    """
    BaseView is an abstract class that defines the structure for all views.
    Views manage the display of data on different types of displays, such as Pixoo.

    Attributes:
        logger (logging.Logger): Logger instance for recording view events.
        display (BaseDisplay): The display to be managed by the view.
        connector (Optional[BaseConnector]): Optional connector for fetching data.
        processor (Optional[BaseProcessor]): Optional processor for transforming data.
        refresh_rate (int): The refresh rate for updating the display in seconds.
        main_color (Tuple[int, int, int]): The main color to be used for rendering.
    """

    def __init__(self, display: BaseDisplay, connector: Optional[BaseConnector] = None, processor: Optional[BaseProcessor] = None, refresh_rate: int = 60, main_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Initializes the BaseView with the given display, connector, processor, and refresh rate.

        Args:
            display (BaseDisplay): The display to be managed by the view.
            connector (Optional[BaseConnector]): Optional connector for fetching data.
            processor (Optional[BaseProcessor]): Optional processor for transforming data.
            refresh_rate (int): The refresh rate for updating the display in seconds.
            main_color (Tuple[int, int, int]): The main color to be used for rendering.
        """
        self.logger = logging.getLogger(__name__)
        self.display = display
        self.connector = connector
        self.processor = processor
        self.refresh_rate = refresh_rate
        self.main_color = main_color

    def refresh(self) -> None:
        """
        Refresh the view by updating the display with new data.

        This method should be implemented by subclasses.
        """
        raise NotImplementedError("The refresh method must be implemented in subclass.")

    def run(self) -> None:
        """
        Run the view, refreshing the display at the specified refresh rate.
        """
        while True:
            self.refresh()
            time.sleep(self.refresh_rate)
