# pixel_kpi/components/line_chart.py
from PIL import Image, ImageDraw
import numpy as np
from ..displays.base_display import BaseDisplay
from typing import List, Tuple

class LineChart:

    @staticmethod
    def draw(display: BaseDisplay, position: Tuple[int, int], x_values: List[float], y_values: List[float], line_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draws a pixel-art line chart on the display.

        Args:
            display (BaseDisplay): The display object where the chart will be rendered.
            position (Tuple[int, int]): The starting position (x, y) of the chart.
            x_values (List[float]): A list of x-coordinates.
            y_values (List[float]): A list of y-coordinates.
            line_color (Tuple[int, int, int]): RGB color of the line.

        Returns:
            None

        Raises:
            ValueError: If x_values and y_values are not of the same length.
        """
        if len(x_values) != len(y_values):
            raise ValueError("x_values and y_values must have the same length.")

        img = Image.fromarray(display.screen)
        draw = ImageDraw.Draw(img)

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        x_scaled = [int((x - x_min) / (x_max - x_min) * (display.width - 1)) for x in x_values]
        y_scaled = [int((1 - (y - y_min) / (y_max - y_min)) * (display.height - 1)) for y in y_values]

        for i in range(len(x_scaled) - 1):
            draw.line((x_scaled[i], y_scaled[i], x_scaled[i + 1], y_scaled[i + 1]), fill=line_color)

        display.screen = np.array(img)
        display.logger.info(f"Drew line chart with {len(x_values)} points.")
