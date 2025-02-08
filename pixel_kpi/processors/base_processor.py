# pixel_kpi/processors/base_processor.py
import logging

class BaseProcessor:
    """
    BaseProcessor is an abstract base class for processing data.

    Attributes:
        logger (logging.Logger): Logger instance for recording processor events.
    """

    def __init__(self) -> None:
        """Initializes a BaseProcessor with a logger."""
        self.logger = logging.getLogger(__name__)
