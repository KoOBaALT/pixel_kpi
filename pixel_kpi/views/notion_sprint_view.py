# pixel_kpi/views/notion_sprint_view.py
from ..displays.base_display import BaseDisplay
from .base_view import BaseView
from ..components.progress_bar import ProgressBar
from ..components.text import Text
from ..connectors.notion_connector import NotionConnector
from ..processors.notion.sprint_processor import SprintProcessor
from typing import Dict, Tuple

class NotionSprintView(BaseView):
    """
    NotionSprintView displays sprint information fetched from a Notion database on the display.
    """

    def __init__(self, display: BaseDisplay, connector: NotionConnector, processor: SprintProcessor, main_color: Tuple[int, int, int], refresh_rate: int = 60*15) -> None:
        """
        Initializes the NotionSprintView with the specified display, connector, processor, and main color.

        Args:
            display (BaseDisplay): The display to render sprint data on.
            connector (NotionConnector): The Notion connector for fetching sprint data.
            processor (SprintProcessor): The processor for handling sprint data.
            main_color (Tuple[int, int, int]): The main color for rendering.
            refresh_rate (int): The refresh rate for updating the display.
        """
        super().__init__(display, connector, processor, refresh_rate, main_color)

    def _get_sprint_data(self) -> Dict[str, any]:
        """
        Fetches and processes sprint data from Notion.

        Returns:
            Dict[str, any]: Contains sprint details like name, dates, and progress.
        """
        filter_data = {
            "filter": {
                "property": "Sprint status",
                "status": {
                    "equals": "Current"
                }
            }
        }

        current_sprint_raw_data = self.connector.query_database(filter_data=filter_data)
        current_sprint_infos = self.processor.extract_sprint_data(current_sprint_raw_data)
        tasks_data_raw = self.connector.get_page(page_id=current_sprint_infos["id"], properties="notion%3A%2F%2Fsprints%2Fcompleted_tasks_property")
        tasks_data_infos = self.processor.extract_task_completion(tasks_data_raw)

        return {**current_sprint_infos, **tasks_data_infos}

    def draw_view(self, sprint_data: Dict[str, any]) -> None:
        """
        Draws the sprint progress view on the display.

        Args:
            sprint_data (Dict[str, any]): The processed sprint data.
        """
        Text.draw(display=self.display, text=sprint_data["name"], position=(2, 2), color=self.main_color)
        ProgressBar.draw(display=self.display, progress=sprint_data["time_progress"], title=f'Days left: {sprint_data["days_until_end"]}', position=(2, 15), color=self.main_color)
        ProgressBar.draw(display=self.display, progress=sprint_data["task_progress"], title=f'Tickets: {sprint_data["completed_tasks"]}/{sprint_data["total_tasks"]}', position=(2, 40), color=self.main_color)

    def refresh(self) -> None:
        """
        Refreshes the sprint view with updated data from Notion.
        """
        sprint_data = self._get_sprint_data()
        self.logger.info(f"Refreshing view with sprint data: {sprint_data}")
        self.display.clear()
        self.draw_view(sprint_data)
        self.display.render()
