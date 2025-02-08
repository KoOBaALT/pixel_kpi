# pixel_kpi/components/text.py
from pixoo.constants.font import retrieve_glyph
from ..displays.base_display import BaseDisplay
from typing import Tuple, Optional

class Text:
    
    @staticmethod
    def draw(display: BaseDisplay, text: str, position: Tuple[int, int] = (1, 1), color: Tuple[int, int, int] = (256, 256, 256), font: Optional[str] = None) -> None:
        """
        Draws text on the Pixoo display.

        Args:
            display (BaseDisplay): The display object where the text will be rendered.
            text (str): The text string to be displayed.
            position (Tuple[int, int]): The (x, y) starting position of the text.
            color (Tuple[int, int, int]): RGB color of the text.
            font (Optional[str]): Font to be used (if any).

        Returns:
            None
        """
        current_position = list(position)
        for i, character in enumerate(text):
            matrix = retrieve_glyph(character)
            if matrix is not None:
                for index, bit in enumerate(matrix):
                    if bit == 1:
                        local_x = index % 3
                        local_y = int(index / 3)
                        display.screen[current_position[1] + local_y, current_position[0] + local_x] = color
            current_position[0] += 4
