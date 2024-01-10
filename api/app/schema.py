from typing import Literal

from pydantic import BaseModel


class Property(BaseModel):
    type: Literal["casa", "departamento"]
    sector: Literal[
        "la reina",
        "las condes",
        "vitacura",
        "lo barnechea",
        "nunoa",
        "providencia",
        "vitacura",
    ]
    net_usable_area: float
    net_area: float
    n_rooms: int
    n_bathroom: int
    latitude: float
    longitude: float
