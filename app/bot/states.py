from enum import IntEnum

class TripState(IntEnum):
    ORIGIN = 1
    DESTINATION = 2
    DEPARTURE_DATE = 3
    RETURN_DATE = 4
    ADULTS = 5
    BUDGET = 6