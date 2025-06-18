from __future__ import annotations

from pydantic import BaseModel, Field


class ItineraryElement(BaseModel):
    """
    Represents a row in an itinerary.
    """

    time: str = Field(..., description="Time of the event in HH:MM format")
    title: str = Field(..., description="Title of the event")
    details: str = Field(..., description="Description of the event")
    icon: str = Field(default="icon.png", description="Icon representing the event")
