import json
from logging import Logger
from pathlib import Path
from typing import Any, Dict

from ...__settings import settings
from ...controllers.itinerary.models.itinerary import ItineraryElement


class ItineraryGetElementsController:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    def get_element(self, itinerary_id: int) -> ItineraryElement:
        """
        Retrieves the elements of an itinerary by its ID.

        :param itinerary_id: The ID of the itinerary to retrieve elements for.
        :return: A list of elements in the itinerary.
        """
        elements: list[ItineraryElement] = self.read_from_file()
        if not elements:
            self.logger.warning("No itinerary elements found in the file.")
            return ItineraryElement(id=itinerary_id, time="", title="", details="")

        return [e for e in elements if e.id == itinerary_id][0]

    def read_from_file(self) -> list[ItineraryElement]:
        """
        Reads the itinerary elements from a JSON file.
        """
        self.logger.info("Reading itinerary elements from file.")
        file_path = Path(settings.text.FULL_PATH).resolve()

        if not file_path.exists():
            self.logger.error(f"Itinerary file not found at: {file_path}")
            raise FileNotFoundError(f"Itinerary file not found at: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            data: Dict[str, Any] = json.load(file)
            return [ItineraryElement(**item) for item in data["itinerary"]]
