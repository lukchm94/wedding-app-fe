from logging import Logger
from typing import Optional, Union

from .....shared.utils.__validations import MenuChoices
from ...domain.guest import Guest
from ...domain.service import GuestService
from .input.rsvp_form import ProcessedRSVPForm, RSVPFormData
from .output.saved_guests import SavedGuests


class SaveRSVPUseCase:
    logger: Logger
    guest_service: GuestService

    def __init__(self, logger: Logger, guest_service: GuestService) -> None:
        self.logger: Logger = logger
        self.guest_service: GuestService = guest_service

    def execute(
        self, rsvp_form: RSVPFormData, guest_id: int, plus_one_id: Optional[int]
    ) -> SavedGuests:

        processed_form: ProcessedRSVPForm = self._process_form(
            rsvp_form, guest_id, plus_one_id
        )

        main_guest_updated: Guest = self._update_guest(processed_form.guest)

        if processed_form.plus_one is not None:
            plus_one_updated: Guest = self._update_guest(processed_form.plus_one)
            return SavedGuests(guest=main_guest_updated, plus_one=plus_one_updated)

        return SavedGuests(guest=main_guest_updated, plus_one=None)

    def _update_guest(self, guest: Guest) -> Guest:
        self.logger.info(f"Updating information for guest: {guest}")
        updated_guest: Guest = self.guest_service.update_guest(guest)
        self.logger.info(f"[OK]: successfully updated guest: {updated_guest}")
        return updated_guest

    def _process_form(
        self, rsvp_form: RSVPFormData, guest_id: int, plus_one_id: Optional[int]
    ) -> ProcessedRSVPForm:
        # Create Guest and ProcessedRSVPForm objects
        guest = Guest(
            id=guest_id,
            first_name=rsvp_form.first_name,
            last_name=rsvp_form.last_name,
            has_guest=rsvp_form.has_guest,
            guest_id=plus_one_id,
            menu=MenuChoices(rsvp_form.menu),
            dietary_requirements=rsvp_form.dietary_requirements,
            needs_hotel=rsvp_form.needs_hotel,
            phone=rsvp_form.phone,
            email=rsvp_form.email,
        )

        plus_one = (
            None
            if not plus_one_id
            else Guest(
                id=plus_one_id,
                first_name=rsvp_form.plus_one_first_name,
                last_name=rsvp_form.plus_one_last_name,
                has_guest=rsvp_form.has_guest,
                guest_id=guest_id,
                menu=(
                    MenuChoices(rsvp_form.plus_one_menu)
                    if rsvp_form.plus_one_menu
                    else None
                ),
                dietary_requirements=rsvp_form.plus_one_dietary_requirements,
                needs_hotel=rsvp_form.needs_hotel,
                phone=rsvp_form.plus_one_phone,
                email=rsvp_form.plus_one_email,
            )
        )

        return ProcessedRSVPForm(guest=guest, plus_one=plus_one)
