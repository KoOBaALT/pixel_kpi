# pixel_kpi/connectors/base_connector.py
import logging

class BaseConnector:
    """
    BaseConnector is an abstract base class for API connectors.

    Attributes:
        logger (logging.Logger): Logger instance for recording connector events.
    """

    def __init__(self) -> None:
        """Initializes a BaseConnector with a logger."""
        self.logger = logging.getLogger(__name__)
