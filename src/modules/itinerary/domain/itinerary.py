from __future__ import annotations

from pydantic import BaseModel, Field


class Itinerary(BaseModel):
    """
    Represents a row in an itinerary.
    """

    id: int = Field(..., description="Unique identifier for the itinerary row")
    time: str = Field(..., description="Time of the event in HH:MM format")
    title: str = Field(..., description="Title of the event")
    details: str = Field(..., description="Description of the event")
    icon: str = Field(default="icon.png", description="Icon representing the event")
    order: int = Field(
        default=0, description="Order of the event in the itinerary"
    )  # Provide default order
    is_active: bool = Field(
        default=True, description="Indicates if the event is currently active"
    )  # Provide default active status
