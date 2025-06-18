from abc import ABC, abstractmethod
from typing import Optional

from .itinerary import Itinerary


class ItineraryRepository(ABC):
    """
    Interface for the Itinerary repository.
    This class defines the methods that any Itinerary repository should implement.
    """

    @abstractmethod
    def get_itinerary(
        self, id: Optional[int] = None, title: Optional[str] = None
    ) -> Itinerary:
        """
        Retrieve an itinerary by its ID.

        :param itinerary_id: The ID of the itinerary to retrieve.
        :return: An Itinerary object.
        """
        pass

    @abstractmethod
    def get_all_itineraries(self, show_active: bool) -> list[Itinerary]:
        """
        Retrieve all itineraries.

        :return: A list of Itinerary, each representing an itinerary.
        """
        pass

    @abstractmethod
    def add_itinerary(self, itinerary: Itinerary) -> Itinerary:
        """
        Save an itinerary to the repository.
        :param itinerary: An Itinerary object to save.
        :return: The saved Itinerary object.
        """
        pass

    @abstractmethod
    def save_all_itineraries(self, itineraries: list[Itinerary]) -> list[Itinerary]:
        """
        Save multiple itineraries to the repository.

        :param itineraries: A list of dictionaries, each representing an itinerary to save.
        """
        pass

    @abstractmethod
    def delete_itinerary(self, id: int) -> None:
        """
        Delete an itinerary by its ID.

        :param itinerary_id: The ID of the itinerary to delete.
        """
        pass

    @abstractmethod
    def update_itinerary(self, itinerary: Itinerary) -> Itinerary:
        """
        Update an existing itinerary.

        :param itinerary: An Itinerary object with updated information.
        :return: The updated Itinerary object.
        """
        pass
