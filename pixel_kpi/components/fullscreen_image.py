# pixel_kpi/components/fullscreen_image.py
from PIL import Image
from ..displays.base_display import BaseDisplay
import numpy as np
from typing import Tuple

class FullscreenImage:
    
    @staticmethod
    def draw(display: BaseDisplay, path: str) -> None:
        """
        Draws a fullscreen image on the Pixoo display.

        Args:
            display (BaseDisplay): The display object where the image will be rendered.
            path (str): The path to the image file.

        Returns:
            None
        """
        img = Image.open(path)
        img_array = np.array(img)[:, :, :3]
        img = Image.fromarray(img_array)
        img_rescaled = img.resize((display.width, display.height), Image.Resampling.LANCZOS)
        display.screen = np.array(img_rescaled)
        display.logger.info(f"Loaded image from {path}")
