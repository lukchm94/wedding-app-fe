from logging import Logger
from typing import List

from pydantic import BaseModel


class ScheduleItem(BaseModel):
    title: str
    details: str
    time: str
    icon: str


class SchedulePayload(BaseModel):
    schedule: List[ScheduleItem]


class ItineraryController:
    def __init__(self, logger: Logger) -> None:
        self.logger: Logger = logger

    def upload(self, payload: SchedulePayload) -> None:
        pass
