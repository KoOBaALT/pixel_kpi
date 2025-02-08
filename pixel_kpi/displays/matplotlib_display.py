# pixel_kpi/displays/matplotlib_display.py
import matplotlib.pyplot as plt
from .base_display import BaseDisplay
from typing import Tuple
from IPython.display import clear_output


class MatplotlibDisplay(BaseDisplay):
    """
    MatplotlibDisplay renders pixel data using the Matplotlib library.

    Inherits from BaseDisplay and adds a method to render the screen contents using Matplotlib.
    """

    def __init__(self, display_name: str, display_id: str, width: int, height: int, background_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Initializes the MatplotlibDisplay with the specified dimensions and background color.

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
        Renders the screen contents using Matplotlib.
        """
        # Clear the output to avoid displaying multiple images
        clear_output()

        # Clear the current figure to avoid multiple plots
        plt.close('all')  # Close all open figures before rendering a new one

        # Create a new figure and set the figure size
        plt.figure(figsize=(5, 5))  # Adjust the figure size to match your display


        # Clear the current figure
        plt.clf()
        if self.screen.shape != (self.height, self.width, 3):
            self.logger.error(f"Data shape mismatch: expected {(self.height, self.width, 3)}, got {self.screen.shape}")
            raise ValueError(f"Data shape must be {(self.height, self.width, 3)}")

        plt.imshow(self.screen)
        plt.axis("off")
        plt.show()

        self.logger.info("Rendered image using Matplotlib.")
