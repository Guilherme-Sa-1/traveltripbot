from app.database.repository import TripRepository
from app.database.models import Trip

class TripService:
    def __init__(self):
        self.repository = TripRepository()

    def register_trip(self, trip_data: dict) -> Trip:
        
        trip = self.repository.save_trip(
            origin=trip_data['origin'],
            destination=trip_data['destination'],
            departure_date=trip_data['departure_date'],
            return_date=trip_data['return_date'],
            adults=trip_data['adults'],
            budget=trip_data['budget']
        )
        return trip

    def get_all_trips(self) -> list[Trip]:

        return self.repository.get_all_trips()
    
    def remove_trip(self, trip_id: int) -> bool:

        return self.repository.delete_trip(trip_id)

    def update_trip_budget(self, trip_id: int, new_budget: float) -> bool:
        
        return self.repository.update_budget(trip_id, new_budget)