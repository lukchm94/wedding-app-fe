from __future__ import annotations

import os

from pydantic import BaseModel, Field

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "itinerary.json")


class ItineraryElement(BaseModel):
    """
    Represents a row in an itinerary.
    """

    id: int = Field(..., description="Unique identifier for the itinerary row")
    time: str = Field(..., description="Time of the event in HH:MM format")
    title: str = Field(..., description="Title of the event")
    details: str = Field(..., description="Description of the event")
    icon: str = Field(
        default="icon.png", description="Icon representing the event"
    )  # Provide default icon
