from app.database.repository import TripRepository
from app.database.models import Trip
from app.services.flight_service import FlightService

class TripService:
    def __init__(self):
        self.repository = TripRepository()
        self.flight_service = FlightService()

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

    def search_flights_for_trip(self, trip_id: int) -> dict:
       
        trip = self.repository.get_trip_by_id(trip_id)
        if not trip:
            return {"success": False, "error": f"Nenhuma viagem encontrada com o ID {trip_id}."}

        try:
            resultado = self.flight_service.search_flights(
                origin=trip.origin,
                destination=trip.destination,
                departure_date=trip.departure_date,
                return_date=trip.return_date,
                adults=trip.adults
            )
            
            if "best_flights" in resultado and len(resultado["best_flights"]) > 0:
                melhor_voo = resultado["best_flights"][0]
                preco = melhor_voo["price"]
                companhia = melhor_voo["flights"][0]["airline"]
                
                return {
                    "success": True,
                    "price": preco,
                    "airline": companhia,
                    "trip": trip 
                }
            else:
                return {"success": False, "error": "O Google Flights não encontrou voos para estas datas ainda."}
                
        except Exception as e:
            return {"success": False, "error": f"Erro ao comunicar com a API: {str(e)}"}