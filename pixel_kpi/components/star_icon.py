
# pixel_kpi/components/star_icon.py
from ..displays.base_display import BaseDisplay
import numpy as np
from typing import Tuple

class StarIcon:
    
    @staticmethod
    def draw(display: BaseDisplay, position: Tuple[int, int] = (0, 0), color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draws a star icon on the Pixoo display.

        Args:
            display (BaseDisplay): The display object where the star will be rendered.
            position (Tuple[int, int]): The (x, y) starting position of the star.
            color (Tuple[int, int, int]): RGB color of the star.

        Returns:
            None
        """
        star_icon = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                              [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                              [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                              [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                              [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
                              [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
                              [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0]])
        
        star_shape = star_icon.shape
        star_icon = np.array([color if pixel == 1 else [0, 0, 0] for pixel in star_icon.flatten()]).reshape(star_shape[0], star_shape[1], 3)
        display.screen[position[0]:position[0] + star_shape[0], position[1]:position[1] + star_shape[1]] = star_icon
