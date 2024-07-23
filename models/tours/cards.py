from pydantic import BaseModel


class get_tour_infoModel(BaseModel):
    tour_id: int

class get_tour_departureModel(BaseModel):
    tour_id: int
    departure_id: int
