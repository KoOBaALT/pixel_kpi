# pixel_kpi/connectors/notion_connector.py
import requests
import json
import logging
from typing import Dict, Any
from .base_connector import BaseConnector

class NotionConnector(BaseConnector):
    """
    A connector for interacting with the Notion API.

    Attributes:
        api_key (str): Notion API token.
        database_id (str): Notion database ID.
        notion_url (str): Base URL for the Notion API.
        headers (Dict[str, str]): Headers for API requests.
    """

    def __init__(self, api_key: str, database_id: str) -> None:
        """
        Initializes the NotionConnector with the provided API key and database ID.

        Args:
            api_key (str): Notion API token.
            database_id (str): Notion database ID.
        """
        super().__init__()
        self.api_key = api_key
        self.database_id = database_id
        self.notion_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def _get(self, url: str) -> Dict[str, Any]:
        """
        Sends a GET request to the Notion API.

        Args:
            url (str): The Notion API URL.

        Returns:
            Dict[str, Any]: Parsed JSON response.

        Raises:
            requests.RequestException: If the GET request fails.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self.logger.info(f"GET request to Notion API successful: {url}")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"GET request failed: {e}")
            raise

    def _post(self, url: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Sends a POST request to the Notion API.

        Args:
            url (str): The Notion API URL.
            data (Dict[str, Any]): Payload for the POST request.

        Returns:
            Dict[str, Any]: Parsed JSON response.

        Raises:
            requests.RequestException: If the POST request fails.
        """
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            self.logger.info(f"POST request to Notion API successful: {url}")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"POST request failed: {e}")
            raise

    def get_page(self, page_id: str, properties: str) -> Dict[str, Any]:
        """
        Fetches a page by its ID from the Notion API.

        Args:
            page_id (str): The Notion page ID.
            properties (str): The properties to include in the response.

        Returns:
            Dict[str, Any]: The page data.
        """
        if properties:
            url = f"{self.notion_url}/pages/{page_id}/properties/{properties}"
        else:
            url = f"{self.notion_url}/pages/{page_id}"
        return self._get(url)

    def query_database(self, filter_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Queries a Notion database with optional filters.

        Args:
            filter_data (Dict[str, Any]): Filter data for the query.

        Returns:
            Dict[str, Any]: Query results from the database.
        """
        url = f"{self.notion_url}/databases/{self.database_id}/query"
        return self._post(url, data=filter_data)
