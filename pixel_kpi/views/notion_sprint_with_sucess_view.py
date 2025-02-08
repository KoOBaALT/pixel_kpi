# pixel_kpi/views/notion_sprint_view.py
from .notion_sprint_view import NotionSprintView
from .firework_view import FireworkView
class NotionSprintViewWithSucess(NotionSprintView):
    """
    NotionSprintView displays sprint information fetched from a Notion database on the display.
    """

    def refresh(self) -> None:
        """
        Refreshes the sprint view with updated data from Notion.
        """
        sprint_data = self._get_sprint_data()
        if sprint_data["task_progress"] >= 1.0:
            self.logger.info("All tasks are completed! Displaying a firework animation.")
            firework_view = FireworkView(display=self.display, headline=sprint_data["name"], subheadline="Completed!", refresh_rate=60*15)
            firework_view.refresh()
            return
        self.logger.info(f"Refreshing view with sprint data: {sprint_data}")
        self.display.clear()
        self.draw_view(sprint_data)
        self.display.render()
