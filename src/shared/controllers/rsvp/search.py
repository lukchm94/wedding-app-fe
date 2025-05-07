from logging import Logger
from typing import Optional, Union

from fastapi import Request
from sqlalchemy.orm import Session

from src.modules.guests.application.find_guest.find_guest_use_case import (
    FindGuestUseCase,
)
from src.shared.database.models.guest import Guest


class SearchController:
    def __init__(
        self, db: Session, find_guest_use_case: FindGuestUseCase, logger: Logger
    ):
        self.db: Session = db
        self.find_guest_use_case: FindGuestUseCase = find_guest_use_case
        self.logger: Logger = logger

    def process_rsvp_form(
        self, request: Request, guest_id: int, plus_one_id: Optional[int] = None
    ) -> dict:
        """
        Process the RSVP form submission.
        """
        guest: Guest = self._find_by_id(guest_id)
        if plus_one_id:
            plus_one = self._find_by_id(plus_one_id)
        elif getattr(guest, "has_guest", False) and getattr(guest, "guest_id", None):
            plus_one = self._find_by_id(guest.guest_id)
        else:
            plus_one = None
        return {
            "request": request,
            "guest": guest,
            "plus_one": plus_one,
        }

    def search(self, first_name: str, last_name: Optional[str] = None) -> list[Guest]:
        """
        Search for guests by first name and optionally last name.

        Args:
            first_name (str): First name of the guest.
            last_name (Optional[str], optional): Last name of the guest. Defaults to None.

        Returns:
            list[Guest]: List of guests found by first name and optionally last name.
        """
        results: list[Guest] = (
            self._find_by_name(first_name, last_name)
            if last_name
            else self._find_in_session(first_name)
        )
        return results

    def _find_in_session(self, first_name: str) -> list[Guest]:
        """
        Find guests in the session by first name.

        Args:
            first_name (str): First name of the guest.

        Returns:
            list[Guest]: List of guests found by first name.
        """
        guests: list[Guest] = self.find_guest_use_case.find_in_session(first_name)

    def _find_by_name(self, first_name: str, last_name: str) -> list[Guest]:
        """
        Find guests by first name and optionally last name.

        Args:
            first_name (str): First name of the guest.
            last_name (str): Last name of the guest.
        """
        guest: Union[Guest, None] = self.find_guest_use_case.execute(
            first_name=first_name, last_name=last_name
        )
        self.logger.info(f"Guest in the controller: {guest}")
        results: list[Guest] = []
        if not guest:
            return results
        results.append(guest)
        plus_one: Union[Guest, None] = self._find_by_id(guest.guest_id)
        if plus_one:
            results.append(plus_one)
        return results

    def _find_by_id(self, guest_id: int) -> Union[Guest, None]:
        """
        Find a guest by their ID.

        Args:
            guest_id (int): The ID of the guest to find.

        Returns:
            Union[Guest, None]: The guest found by their ID.
        """
        guest: Union[Guest, None] = self.find_guest_use_case.execute(guest_id=guest_id)
        return guest
