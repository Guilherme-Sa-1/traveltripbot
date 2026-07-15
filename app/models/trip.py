from dataclasses import dataclass


@dataclass
class Trip:
    origin: str
    destination: str
    departure_date: str
    return_date: str
    adults: int
    budget: float