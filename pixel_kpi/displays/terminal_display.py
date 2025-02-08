# pixel_kpi/displays/terminal_display.py
import numpy as np
from PIL import Image
from .base_display import BaseDisplay
from typing import Tuple

class TerminalDisplay(BaseDisplay):
    """
    TerminalDisplay renders pixel data in the terminal using grayscale characters.

    Inherits from BaseDisplay and adds functionality to render the display contents in a terminal.
    """

    def __init__(self, display_name: str, display_id: str, width: int, height: int, background_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Initializes the TerminalDisplay with the specified dimensions and background color.

        Args:
            display_name (str): Name of the display.
            display_id (str): ID of the display.
            width (int): Width of the display in pixels.
            height (int): Height of the display in pixels.
            background_color (Tuple[int, int, int]): RGB tuple representing the background color.
        """
        super().__init__(display_name, display_id, width, height, background_color)

    def render(self) -> None:
        """
        Renders the image stored in `self.screen` as a grayscale image in the terminal.
        """
        if self.screen.shape != (self.height, self.width, 3):
            self.logger.error(f"Data shape mismatch: expected {(self.height, self.width, 3)}, got {self.screen.shape}")
            raise ValueError(f"Data shape must be {(self.height, self.width, 3)}")

        grayscale = (0.299 * self.screen[:, :, 0] + 0.587 * self.screen[:, :, 1] + 0.114 * self.screen[:, :, 2]).astype(np.uint8)

        aspect_ratio = 1.0
        new_width = self.width
        new_height = int(self.height * aspect_ratio)
        grayscale_resized = Image.fromarray(grayscale).resize((new_width, new_height))
        grayscale = np.array(grayscale_resized)

        chars = " .:-=+*#%@"
        char_len = len(chars)

        indices = (grayscale / 255) * (char_len - 1)
        indices = indices.astype(int)

        lines = ["".join([chars[pixel] for pixel in row]) for row in indices]
        terminal_image = "\n".join(lines)

        print(terminal_image)
        self.logger.info("Rendered image to terminal.")
