from logging import Logger
from typing import List

from ...domain.itinerary import Itinerary
from ...domain.itinerary_service import ItineraryService


class UploadItineraryUseCase:
    def __init__(self, service: ItineraryService, logger: Logger) -> None:
        self.service: ItineraryService = service
        self.logger: Logger = logger

    def execute(self, data: List[Itinerary]) -> None:
        """
        Uploads an itinerary to the repository.

        :param itinerary_data: The data of the itinerary to be uploaded.
        :return: The result of the upload operation.
        """
        self.logger.debug(f"Uploading itinerary: {[d.model_dump() for d in data]}")
