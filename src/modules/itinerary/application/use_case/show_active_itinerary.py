from logging import Logger
from typing import List

from ...domain.itinerary import Itinerary
from ...domain.itinerary_service import ItineraryService
from ..output.displayed_itinerary import ItineraryElement


class ShowActiveItineraryUseCase:
    def __init__(self, service: ItineraryService, logger: Logger) -> None:
        self.service: ItineraryService = service
        self.logger: Logger = logger

    def execute(self, show_active: bool) -> List[ItineraryElement]:
        """
        Retrieves the active itinerary for a given user.

        :param user_id: The ID of the user whose active itinerary is to be retrieved.
        :return: The active itinerary for the user, or None if no active itinerary exists.
        """
        active_itinerary: List[Itinerary] = self.service.get_active_itinerary(
            show_active
        )

        active_itinerary.sort(key=lambda x: x.order)

        return [
            ItineraryElement(
                title=itinerary.title,
                details=itinerary.details,
                time=itinerary.time,
                icon=itinerary.icon,
            )
            for itinerary in active_itinerary
        ]
