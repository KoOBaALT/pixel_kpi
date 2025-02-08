# pixel_kpi/processors/notion/sprint_processor.py
from datetime import datetime
from typing import Dict, Any, Tuple
from ..base_processor import BaseProcessor

class SprintProcessor(BaseProcessor):
    """
    A processor for handling sprint-related data from Notion.

    Attributes:
        DATE_FORMAT (str): Expected date format for parsing dates.
    """

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self) -> None:
        """Initializes the SprintProcessor."""
        super().__init__()

    def extract_sprint_data(self, sprint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts essential sprint information from the provided sprint data.

        Args:
            sprint_data (Dict[str, Any]): Raw sprint data fetched from Notion.

        Returns:
            Dict[str, Any]: Sprint ID, name, start date, end date, days until end, and time progress.

        Raises:
            ValueError: If sprint data is in an invalid format.
        """
        self.logger.info("Processing sprint data")
        try:
            sprint_info = sprint_data["results"][0]
            sprint_id = sprint_info["id"]
            name = self._get_sprint_name(sprint_info)
            start_date_str, end_date_str = self._get_sprint_dates(sprint_info)
            days_until_end, time_progress = self.calculate_time_left(start_date_str, end_date_str)
        except (IndexError, KeyError, TypeError) as e:
            self.logger.error(f"Error extracting sprint data: {e}")
            raise ValueError("Invalid sprint data format.")

        return {
            "id": sprint_id, 
            "name": name, 
            "start_date_str": start_date_str, 
            "end_date_str": end_date_str,
            "days_until_end": days_until_end,
            "time_progress": time_progress
        }

    def extract_task_completion(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts sprint progress based on task completion.

        Args:
            task_data (Dict[str, Any]): Task data of a sprint fetched from Notion.

        Returns:
            Dict[str, Any]: Sprint progress, total tasks, and completed tasks.
        """
        self.logger.info("Calculating sprint progress from task data")
        tasks = task_data.get("results", [])
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.get("status", {}).get("id") == "done")

        if total_tasks == 0:
            self.logger.warning("No tasks found in the sprint data")
            task_progress = 0.0
        else:
            task_progress = completed_tasks / total_tasks

        self.logger.info(f"Sprint progress: {completed_tasks}/{total_tasks} tasks completed")
        return {
            "task_progress": task_progress,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks
        }

    def calculate_time_left(self, start_date: str, end_date: str) -> Tuple[int, float]:
        """
        Calculates the remaining time in the sprint and its progress.

        Args:
            start_date (str): Sprint start date in "YYYY-MM-DD" format.
            end_date (str): Sprint end date in "YYYY-MM-DD" format.

        Returns:
            Tuple[int, float]: Days until sprint end and percentage of total time passed.

        Raises:
            ValueError: If the start date is after the end date.
        """
        self.logger.info("Calculating time left in the sprint")
        start_datetime = self._parse_date(start_date, "start_date")
        end_datetime = self._parse_date(end_date, "end_date")

        if start_datetime >= end_datetime:
            self.logger.error("Start date must be before end date")
            raise ValueError("Start date must be before end date.")

        current_time = datetime.now()
        days_until_end = (end_datetime - current_time).days
        total_sprint_duration = (end_datetime - start_datetime).total_seconds()
        time_elapsed = (current_time - start_datetime).total_seconds()

        if total_sprint_duration <= 0:
            self.logger.warning("Sprint duration is zero or negative")
            sprint_time_progress = 0.0
        else:
            sprint_time_progress = time_elapsed / total_sprint_duration

        sprint_time_progress = max(0.0, min(sprint_time_progress, 1.0))

        self.logger.info(f"Time left: {days_until_end} days, {sprint_time_progress * 100:.2f}% time passed")
        return days_until_end, sprint_time_progress

    def _parse_date(self, date_str: str, field_name: str) -> datetime:
        """
        Parses a date string into a datetime object.

        Args:
            date_str (str): Date string in the expected format.
            field_name (str): Name of the date field for logging purposes.

        Returns:
            datetime: Parsed datetime object.

        Raises:
            ValueError: If the date format is incorrect.
        """
        try:
            parsed_date = datetime.strptime(date_str, self.DATE_FORMAT)
            self.logger.debug(f"Parsed {field_name}: {parsed_date}")
            return parsed_date
        except ValueError as e:
            self.logger.error(f"Date format error for {field_name}: {e}")
            raise ValueError(f"Dates should be in '{self.DATE_FORMAT}' format.")

    def _get_sprint_name(self, sprint_info: Dict[str, Any]) -> str:
        """
        Extracts the sprint name from sprint information.

        Args:
            sprint_info (Dict[str, Any]): Sprint information dictionary.

        Returns:
            str: Sprint name.

        Raises:
            ValueError: If the sprint name is missing.
        """
        try:
            sprint_name = sprint_info["properties"]["Sprint name"]["title"][0]["text"]["content"]
            self.logger.debug(f"Extracted sprint name: {sprint_name}")
            return sprint_name
        except (KeyError, IndexError, TypeError) as e:
            self.logger.error(f"Error extracting sprint name: {e}")
            raise ValueError("Sprint name is missing or malformed.")

    def _get_sprint_dates(self, sprint_info: Dict[str, Any]) -> Tuple[str, str]:
        """
        Extracts the start and end dates from sprint information.

        Args:
            sprint_info (Dict[str, Any]): Sprint information dictionary.

        Returns:
            Tuple[str, str]: Start date and end date as strings.

        Raises:
            ValueError: If the dates are missing or malformed.
        """
        try:
            dates = sprint_info["properties"]["Dates"]["date"]
            start_date = dates["start"]
            end_date = dates["end"]
            self.logger.debug(f"Extracted start date: {start_date}, end date: {end_date}")
            return start_date, end_date
        except (KeyError, TypeError) as e:
            self.logger.error(f"Error extracting sprint dates: {e}")
            raise ValueError("Sprint dates are missing or malformed.")
