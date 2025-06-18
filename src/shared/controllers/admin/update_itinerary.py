from logging import Logger
from typing import List

from pydantic import BaseModel

from src.modules.itinerary.application.use_case.upload_itinerary import (
    UploadItineraryUseCase,
)
from src.modules.itinerary.domain.itinerary import Itinerary


class ScheduleItem(BaseModel):
    title: str
    details: str
    time: str
    icon: str


class SchedulePayload(BaseModel):
    schedule: List[ScheduleItem]


class ItineraryController:
    def __init__(self, logger: Logger, use_case: UploadItineraryUseCase) -> None:
        self.logger: Logger = logger
        self.use_case: UploadItineraryUseCase = use_case

    def upload(self, payload: SchedulePayload) -> bool:
        try:
            self.logger.debug(
                f"Uploading itinerary with payload: {payload.model_dump()}"
            )
            itinerary: List[Itinerary] = self._map_payload_to_itinerary(payload)

            self.use_case.execute(itinerary)
            self.logger.info("Itinerary uploaded successfully.")
            return True
        except Exception as err:
            self.logger.error(f"Failed to upload itinerary: {err}")
            return False

    def _map_payload_to_itinerary(self, payload: SchedulePayload) -> List[Itinerary]:
        """
        Maps the SchedulePayload to a list of itinerary dictionaries.
        """
        return [
            Itinerary(
                id=None,  # ID will be set by the database
                title=item.title,
                details=item.details,
                time=item.time,
                icon=item.icon,
            )
            for item in payload.schedule
        ]
