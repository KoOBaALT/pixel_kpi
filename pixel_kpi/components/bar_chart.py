# pixel_kpi/components/bar_chart.py
from ..displays.base_display import BaseDisplay
from .text import Text
from typing import List, Tuple, Optional

class BarChart:
    
    @staticmethod
    def draw(display: BaseDisplay, data: List[float], labels: Optional[List[str]] = None, position: Tuple[int, int] = (2, 15), max_height: int = 10, bar_width: int = 4, spacing: int = 2, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draws a bar chart on the Pixoo display.

        Args:
            display (BaseDisplay): The display object where the chart will be rendered.
            data (List[float]): List of numerical values representing the bar heights.
            labels (Optional[List[str]]): Optional list of labels for each bar.
            position (Tuple[int, int]): Starting position (x, y) of the chart on the display.
            max_height (int): Maximum height of the bars in pixels.
            bar_width (int): Width of each bar in pixels.
            spacing (int): Space between the bars in pixels.
            color (Tuple[int, int, int]): RGB color of the bars and labels.

        Returns:
            None
        """
        max_value = max(data)
        max_value = max(max_value, 1)  # Avoid division by zero
        normalized_data = [value / max_value for value in data]

        for i, value in enumerate(normalized_data):
            bar_height = min(int(value * max_height), max_height)
            for y in range(bar_height):
                for x in range(bar_width):
                    display.screen[position[1] + max_height - y, position[0] + i * (bar_width + spacing) + x] = color
            
            if labels and i < len(labels):
                label_width = len(labels[i]) * 3
                bar_center = position[0] + i * (bar_width + spacing) + (bar_width // 2)
                label_position = bar_center - (label_width // 2)
                Text.draw(display, labels[i], (label_position, position[1] + max_height + 2), color)
