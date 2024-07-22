from pydantic import BaseModel


class get_tour_infoModel(BaseModel):
    tour_id: int
