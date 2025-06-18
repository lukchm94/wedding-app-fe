from ..domain.itinerary import Itinerary
from ..infrastructure.repository.os.os_itinerary_impl import (
    OsItineraryRepositoryImplementation,
)


class ItineraryService:
    def __init__(self, itinerary_repository: OsItineraryRepositoryImplementation):

        self.itinerary_repository: OsItineraryRepositoryImplementation = (
            itinerary_repository
        )

    def get_all_itineraries(self) -> list[Itinerary]:
        """
        Retrieve all itineraries from the repository.

        :return: A list of all itineraries.
        """
        return self.itinerary_repository.get_all_itineraries()
