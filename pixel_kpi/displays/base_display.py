# pixel_kpi/displays/base_display.py
import logging
import numpy as np
from typing import Tuple

class BaseDisplay:
    """
    BaseDisplay is an abstract class that provides basic functionality for a display,
    including pixel manipulation and screen clearing.

    Attributes:
        display_name (str): Name of the display.
        display_id (str): ID of the display.
        width (int): Width of the display in pixels.
        height (int): Height of the display in pixels.
        background_color (Tuple[int, int, int]): RGB tuple representing the background color.
        screen (np.ndarray): 3D NumPy array representing the pixel data of the display.
        logger (logging.Logger): Logger instance for recording display events.
    """

    def __init__(self, display_name: str, display_id: str, width: int = 64, height: int = 64, background_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Initializes the BaseDisplay with the specified dimensions and background color.

        Args:
            display_name (str): Name of the display.
            display_id (str): ID of the display.
            width (int): Width of the display in pixels.
            height (int): Height of the display in pixels.
            background_color (Tuple[int, int, int]): RGB tuple representing the background color.
        """
        self.display_name = display_name
        self.display_id = display_id
        self.width = width
        self.height = height
        self.background_color = background_color
        self.screen = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.logger = logging.getLogger(__name__)

    def clear(self) -> None:
        """
        Clears the display by setting all pixels to the background color.
        """
        self.screen.fill(0)
        self.screen[:, :] = self.background_color
        self.logger.info("Cleared the display")
