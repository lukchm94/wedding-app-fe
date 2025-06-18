import json
from logging import Logger
from pathlib import Path
from typing import Any, Dict, Optional

from ......shared.__settings import Settings
from ....domain.itinerary import Itinerary
from ....domain.itinerary_repo import ItineraryRepository


class OsPaths:
    def __init__(self, settings: Settings) -> None:
        self.settings: Settings = settings

    @property
    def full_path(self) -> str:
        """Returns the full path to the itinerary file."""
        return self.settings.text.FULL_PATH

    @property
    def resolved(self) -> Path:
        """Returns the resolved path to the itinerary file."""
        return Path(self.settings.text.FULL_PATH).resolve()


class OsItineraryRepositoryImplementation(ItineraryRepository):
    def __init__(self, logger: Logger, paths: OsPaths) -> None:
        self.logger: Logger = logger
        self.paths: OsPaths = paths
        self.logger.info(
            f"[{self.__class__.__name__}] initialized with itinerary path: {self.paths.full_path}"
        )

    def get_itinerary(
        self, id: Optional[int] = None, title: Optional[str] = None
    ) -> Itinerary:
        self.logger.debug(
            f"[{self.__class__.__name__}] get_itinerary called with id: {id}, title: {title}"
        )
        if id is not None:
            return self._get_from_id(id)
        if title is not None:
            return self._get_from_title(title)

        raise ValueError(
            f"[{self.__class__.__name__}] Either id or title must be provided to get_itinerary. Received id: {id}, title: {title}"
        )

    def get_all_itineraries(self, show_active: bool) -> list[Itinerary]:
        self.logger.debug(f"[{self.__class__.__name__}] get_all_itineraries called.")
        existing_itineraries: list[Itinerary] = self._read_and_convert_to_itineraries()
        self.logger.info(
            f"[{self.__class__.__name__}] Found {len(existing_itineraries)} itineraries."
        )
        return [i for i in existing_itineraries if i.is_active == show_active]

    def add_itinerary(self, itinerary: Itinerary) -> Itinerary:
        current_itineraries: list[Itinerary] = self._read_and_convert_to_itineraries()
        self.logger.debug(f"[{self.__class__.__name__}] Adding itinerary: {itinerary}")
        current_itineraries.append(itinerary)
        return itinerary

    def save_all_itineraries(self, itineraries: list[Itinerary]) -> list[Itinerary]:
        self.logger.debug(
            f"[{self.__class__.__name__}] save_all_itineraries called with {len(itineraries)} itineraries."
        )
        self._write_to_file(itineraries)
        return itineraries

    def delete_itinerary(self, id: int) -> None:
        self.logger.debug(
            f"[{self.__class__.__name__}] delete_itinerary called with id: {id}"
        )
        current_itineraries: list[Itinerary] = self._read_and_convert_to_itineraries()
        to_persist: list[Itinerary] = [i for i in current_itineraries if i.id != id]
        self._write_to_file(to_persist)

    def update_itinerary(self, itinerary: Itinerary) -> Itinerary:
        # Logic to update an existing itinerary in the database
        self.logger.warning(
            f"[{self.__class__.__name__}] update_itinerary method is not implemented."
        )
        return itinerary

    def _read_and_convert_to_itineraries(self) -> list[Itinerary]:
        """
        Reads the itinerary data from the file and converts it to a list of Itinerary objects.
        This is a placeholder for actual implementation.
        """
        self.logger.debug(f"[{self.__class__.__name__}] Reading itineraries from file.")
        # Simulating reading from a file and converting to Itinerary objects
        if not self.paths.resolved.exists():
            self.logger.error(f"Itinerary file not found at: {self.paths.resolved}")
            raise FileNotFoundError(
                f"[{self.__class__.__name__}] Itinerary file not found at: {self.paths.resolved}"
            )

        with open(self.paths.resolved, "r", encoding="utf-8") as file:
            data: Dict[str, Any] = json.load(file)
            return [
                Itinerary(**item)
                for item in data[self.paths.settings.text.ITINERARY_KEY]
            ]

    def _get_from_id(self, id: int) -> Itinerary:
        """
        Helper method to create an Itinerary object from an ID.
        This is a placeholder for actual implementation.
        """
        self.logger.debug(
            f"[{self.__class__.__name__}] Creating itinerary from ID: {id}"
        )
        itineraries: list[Itinerary] = self._read_and_convert_to_itineraries()
        return [i for i in itineraries if i.id == id][0]

    def _get_from_title(self, title: str) -> Itinerary:
        """
        Helper method to create an Itinerary object from a title.
        This is a placeholder for actual implementation.
        """
        self.logger.debug(
            f"[{self.__class__.__name__}] Creating itinerary from title: {title}"
        )
        itineraries: list[Itinerary] = self._read_and_convert_to_itineraries()
        return [i for i in itineraries if i.title == title][0]

    def _write_to_file(self, itineraries: list[Itinerary]) -> None:
        """
        Writes the list of Itinerary objects to the file.
        This is a placeholder for actual implementation.
        """
        self.logger.debug(f"[{self.__class__.__name__}] Writing itineraries to file.")
        try:
            if self.paths.resolved.parent.exists():
                self.logger.info(
                    f"[{self.__class__.__name__}] directory for itinerary file: {self.paths.resolved.parent} exists. Overriding the current file."
                )

            with open(self.paths.resolved, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        self.paths.settings.text.ITINERARY_KEY: (
                            [i.model_dump() for i in itineraries]
                        )
                    },
                    file,
                    ensure_ascii=False,
                    indent=4,
                )
        except Exception as err:
            self.logger.error(
                f"[{self.__class__.__name__}] Error writing to file: {err}"
            )
            raise err
