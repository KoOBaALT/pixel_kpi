# pixel_kpi/displays/pixoo_display.py
from .base_display import BaseDisplay
import importlib.util
import sys
import logging
from typing import Tuple

# Check if tkinter is available
tkinter_available = importlib.util.find_spec("tkinter") is not None

# Only import Pixoo if tkinter is available
if tkinter_available:
    try:
        from pixoo import Pixoo
        from pixoo.configurations.simulatorconfiguration import SimulatorConfiguration
    except ImportError as e:
        if "_tkinter" in str(e):
            logging.warning("tkinter not found. Install with: 'brew install python-tk' (macOS) or 'apt-get install python3-tk' (Debian/Ubuntu)")
            tkinter_available = False
else:
    logging.warning("tkinter not found. Install with: 'brew install python-tk' (macOS) or 'apt-get install python3-tk' (Debian/Ubuntu)")

class PixooDisplay(BaseDisplay):
    """
    PixooDisplay is designed for managing a Pixoo 64x64 display, supporting both real and simulated hardware.

    Inherits from BaseDisplay and adds functionality for interacting with Pixoo hardware or the Pixoo simulator.
    """

    def __init__(self, display_name: str, display_id: str, ip_address: str, width: int = 64, height: int = 64, background_color: Tuple[int, int, int] = (0, 0, 0), simulated: bool = False) -> None:
        """
        Initializes the PixooDisplay with the specified parameters.

        Args:
            display_name (str): Name of the display.
            display_id (str): ID of the display.
            ip_address (str): IP address of the Pixoo device.
            width (int): Width of the display in pixels (must be 64).
            height (int): Height of the display in pixels (must be 64).
            background_color (Tuple[int, int, int]): RGB tuple representing the background color.
            simulated (bool): Whether to use the Pixoo simulator.
        """
        super().__init__(display_name, display_id, width, height, background_color)

        if self.width != 64 or self.height != 64:
            raise ValueError("Pixoo display must have a resolution of 64x64 pixels.")

        if not tkinter_available:
            raise ImportError(
                "The tkinter module is required for Pixoo display. "
                "Please install it with:\n"
                "- macOS: brew install python-tk\n"
                "- Ubuntu/Debian: sudo apt-get install python3-tk\n"
                "- Fedora: sudo dnf install python3-tkinter\n"
                "Then reinstall this package."
            )
            
        if simulated:
            self.logger.info("Using Pixoo simulator")
            self.pixoo = Pixoo(ip_address, simulated=True, simulation_config=SimulatorConfiguration())
        else:
            self.pixoo = Pixoo(ip_address)

    def clear(self) -> None:
        """
        Clears the display both on the Pixoo hardware and locally.
        """
        self.pixoo.clear()
        super().clear()

    def render(self) -> None:
        """
        Renders the screen contents on the Pixoo hardware.
        """
        self.pixoo.clear()
        for x in range(self.width):
            for y in range(self.height):
                r, g, b = self.screen[y, x]
                self.pixoo.draw_pixel_at_location_rgb(x, y, r, g, b)
        self.pixoo.push()
