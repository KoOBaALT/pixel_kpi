# pixel_kpi/connectors/github_connector.py
# 
# This code is adapted from the GitHub repository: https://github.com/MichaelPap/GitHubStarsHistory
# Original code under MIT License by Michael Papadopoulos
# License URL: https://github.com/MichaelPap/GitHubStarsHistory/blob/master/LICENSE
#
# Some parts of this code (e.g. download_stargazers function) have been reused and modified for this project.
#
from .base_connector import BaseConnector
import requests
import json
import time
from dateutil.parser import parse
from typing import Dict, List, Any

class GithubConnector(BaseConnector):
    """
    A connector for interacting with the GitHub API.

    Attributes:
        api_key (str): GitHub API token.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the GitHubConnector with the provided API key.

        Args:
            api_key (str): GitHub API token.
        """
        super().__init__()
        self.api_key = api_key

    def download_stargazers(self, repository: str) -> Dict[str, int]:
        """
        Downloads stargazers information from a GitHub repository.

        Args:
            repository (str): The GitHub repository in the format 'owner/repo'.

        Returns:
            Dict[str, int]: A dictionary where the keys are 'YYYY-MM' and the values are cumulative stars.
        """
        self.logger.info(f'Downloading Stargazers Info for repository: {repository}')
        stars_info = []
        self.check_limit()

        r = requests.get(f"https://api.github.com/repos/{repository}/stargazers?per_page=100",
                         headers={
                             'Authorization': f'token {self.api_key}',
                             'Accept': 'application/vnd.github.v3.star+json'
                         })
        if r.status_code == 200:
            stars_info.extend(json.loads(r.text or r.content))

            if 'Link' in r.headers:
                last_page = int(r.headers["Link"].split('&page=')[-1].split('>')[0])
                self.logger.info(f'Number of Info Pages: {last_page}')

                for page in range(2, last_page + 1):
                    self.logger.info(f'Downloading Page {page}')
                    self.check_limit()
                    r = requests.get(f"https://api.github.com/repos/{repository}/stargazers?per_page=100&page={page}",
                                     headers={
                                         'Authorization': f'token {self.api_key}',
                                         'Accept': 'application/vnd.github.v3.star+json'
                                     })
                    if r.status_code == 200:
                        stars_info.extend(json.loads(r.text or r.content))

        stars = {}
        for stargazer_info in stars_info:
            timestamp = parse(stargazer_info["starred_at"])
            date_ref = f"{timestamp.year}-{str(timestamp.month).zfill(2)}"
            stars[date_ref] = stars.get(date_ref, 0) + 1

        sorted_keys = sorted(stars.keys())
        for i in range(1, len(sorted_keys)):
            stars[sorted_keys[i]] += stars[sorted_keys[i - 1]]

        return stars

    def check_limit(self) -> None:
        """
        Checks the GitHub API rate limit and waits for reset if necessary.
        """
        r = requests.get("https://api.github.com/rate_limit", headers={'Authorization': f'token {self.api_key}'})
        if r.status_code == 200:
            content = json.loads(r.text or r.content)
            remaining_requests = content["resources"]["core"]["remaining"]
            reset_time = content["resources"]["core"]["reset"]
            if remaining_requests < 1:
                self.wait_for_limit_reset(reset_time)
        else:
            self.logger.info('Check limit query failed... Retry')
            self.check_limit()

    def wait_for_limit_reset(self, reset_time: int) -> None:
        """
        Waits for the API rate limit to reset.

        Args:
            reset_time (int): The time (in epoch seconds) when the rate limit will reset.
        """
        curr_time = time.time()
        sleep_time = int(reset_time - curr_time)
        self.logger.info(f'Rate limit reached... Waiting for {sleep_time + 1} seconds')
        time.sleep(sleep_time + 1)
