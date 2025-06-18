from logging import Logger
from typing import List

from ..domain.itinerary import Itinerary
from ..infrastructure.repository.os.os_itinerary_impl import (
    OsItineraryRepositoryImplementation,
)


class ItineraryService:
    def __init__(
        self, itinerary_repository: OsItineraryRepositoryImplementation, logger: Logger
    ):

        self.itinerary_repository: OsItineraryRepositoryImplementation = (
            itinerary_repository
        )
        self.logger: Logger = logger

    def get_all_itineraries(self) -> list[Itinerary]:
        """
        Retrieve all itineraries from the repository.

        :return: A list of all itineraries.
        """
        return self.itinerary_repository.get_all_itineraries(False)

    def get_active_itinerary(self, show_active: bool) -> list[Itinerary]:
        """
        Retrieve the active itinerary from the repository.

        :return: A list containing the active itinerary.
        """
        return self.itinerary_repository.get_all_itineraries(show_active)

    def add_itinerary(self, itinerary: List[Itinerary]) -> bool:
        try:
            uploaded: List[Itinerary] = self.itinerary_repository.save_all_itineraries(
                itinerary
            )
            self.logger.info(
                f"[{self.__class__.__name__}] Uploaded {len(uploaded)} elements of itinerary successfully."
            )
            return True
        except Exception as err:
            self.logger.error(
                f"[{self.__class__.__name__}] Failed to upload itinerary: {err}"
            )
            return False
