from pydantic import BaseModel
from typing import List

class variationsModel(BaseModel):
    variation: int
    name: str

class reservationModel(BaseModel):
    tour_id: int
    departure_id: int
    name: str
    phone_number: str
    email: str
    messanger: str
    comment: str
    variations: List[variationsModel]