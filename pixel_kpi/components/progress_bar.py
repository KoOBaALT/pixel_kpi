# pixel_kpi/components/progress_bar.py
from ..displays.base_display import BaseDisplay
from .text import Text
from typing import Tuple

class ProgressBar:
    
    @staticmethod
    def draw(display: BaseDisplay, progress: float, title: str = "Progress", position: Tuple[int, int] = (2, 15), color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draws a progress bar on the Pixoo display.

        Args:
            display (BaseDisplay): The display object where the progress bar will be rendered.
            progress (float): The progress value between 0 and 1.
            title (str): The title displayed above the progress bar.
            position (Tuple[int, int]): The (x, y) position of the progress bar on the display.
            color (Tuple[int, int, int]): RGB color of the title and the progress bar.

        Returns:
            None
        """
        Text.draw(display, title, position, color)
        
        if progress < 1: 
            x_offset = 48
        else:
            x_offset = 45

        Text.draw(display, str(round(progress * 100)) + "%", (position[0] + x_offset, position[1] + 8), color)
        
        progress = max(0, min(progress, 1))
        
        bar_length = 9
        filled_length = int(round(bar_length * progress))
        progress_bar = "|" + "=" * filled_length + " " * (bar_length - filled_length) + "|"
        
        Text.draw(display, progress_bar, (position[0], position[1] + 8), color)
