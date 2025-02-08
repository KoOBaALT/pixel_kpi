# pixel_kpi/connectors/github_connector.py

from .base_connector import BaseConnector
import pypistats
from typing import Dict, List, Any
import json

class PyPiConnector(BaseConnector):
    """
    A connector for interacting with the PyPi stats API.
    """

    def __init__(self) -> None:
        """
        Initializes the PyPiConnector.
        """
        super().__init__()

    def get_downloads(self, repository: str) -> Dict[str, int]:
        """
        Downloads stargazers information from a GitHub repository.

        Args:
            repository (str): The GitHub repository in the format 'owner/repo'.

        Returns:
            Dict[str, int]: A dictionary where the keys are 'YYYY-MM' and the values are cumulative stars.
        """
        downloads_str = pypistats.overall(repository, format="json")
        downloads_json = json.loads(downloads_str)
        downloads = downloads_json["data"][1]["downloads"]

        return downloads
