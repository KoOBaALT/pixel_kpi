# pixel_kpi/components/headline.py
from pixoo.constants.font import retrieve_glyph
from ..displays.base_display import BaseDisplay
from typing import Tuple, Optional

class Headline:
    
    @staticmethod
    def draw(display: BaseDisplay, text: str, position: Tuple[int, int] = (1, 1), scale: int = 2, color: Tuple[int, int, int] = (256, 256, 256), font: Optional[str] = None) -> None:
        """
        Draws scaled-up text on the Pixoo display.

        Args:
            display (BaseDisplay): The display object where the text will be rendered.
            text (str): The text string to be displayed.
            position (Tuple[int, int]): The (x, y) starting position of the text.
            scale (int): The scaling factor to increase the size of the text.
            color (Tuple[int, int, int]): The RGB color of the text.
            font (Optional[str]): The font to be used (if any).
        
        Returns:
            None
        """
        current_position = list(position)
        for i, character in enumerate(text):
            matrix = retrieve_glyph(character)
            if matrix is not None:
                for index, bit in enumerate(matrix):
                    if bit == 1:
                        local_x = (index % 3) * scale
                        local_y = (index // 3) * scale
                        for x in range(scale):
                            for y in range(scale):
                                display.screen[current_position[1] + local_y + y, current_position[0] + local_x + x] = color
            current_position[0] += 4 * scale
