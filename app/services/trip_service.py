from datetime import datetime, timedelta
from app.database.repository import TripRepository
from app.services.flight_service import FlightService

class TripService:
    def __init__(self):
        self.repository = TripRepository()
        self.flight_service = FlightService()

    def add_trip(self, origin: str, destination: str, departure_date: str, return_date: str, adults: int, budget: float):
        return self.repository.add_trip(origin, destination, departure_date, return_date, adults, budget)

    def get_all_trips(self):
        return self.repository.get_all_trips()

    def delete_trip(self, trip_id: int) -> bool:
        return self.repository.delete_trip(trip_id)

    def update_budget(self, trip_id: int, new_budget: float) -> bool:
        return self.repository.update_budget(trip_id, new_budget)

    def search_flights_for_trip(self, trip_id: int) -> dict:
        trip = self.repository.get_trip_by_id(trip_id)
        if not trip:
            return {"success": False, "error": f"Nenhuma viagem encontrada com o ID {trip_id}."}

        melhor_preco_da_janela = float('inf')
        voo_escolhido = None
        data_do_voo_escolhido = None
        link_final = ""
        nome_origem = trip.origin
        nome_destino = trip.destination

        data_ida_obj = datetime.strptime(trip.departure_date, "%d/%m/%Y")
        data_volta_obj = datetime.strptime(trip.return_date, "%d/%m/%Y")

        # Busca -1, 0 (hoje) e +1 dia
        for i in range(-1, 2):
            data_ida_atual = data_ida_obj + timedelta(days=i)
            data_volta_atual = data_volta_obj + timedelta(days=i) 

            try:
                resultado = self.flight_service.search_flights(
                    origin=trip.origin,
                    destination=trip.destination,
                    departure_date=data_ida_atual.strftime("%d/%m/%Y"),
                    return_date=data_volta_atual.strftime("%d/%m/%Y"),
                    adults=trip.adults
                )
                if "best_flights" in resultado and len(resultado["best_flights"]) > 0:
                    primeiro_voo = resultado["best_flights"][0]
                    preco = primeiro_voo["price"]

                    if preco < melhor_preco_da_janela:
                        melhor_preco_da_janela = preco
                        voo_escolhido = primeiro_voo
                        data_do_voo_escolhido = data_ida_atual.strftime("%d/%m/%Y")
                        link_final = resultado.get("search_metadata", {}).get("google_flights_url", "")
                        
                        # Extrai os nomes extensos das cidades
                        airports = resultado.get("airports", [{}])[0]
                        if airports:
                            dep_info = airports.get("departure", [])
                            arr_info = airports.get("arrival", [])
                            if dep_info:
                                nome_origem = dep_info[0].get('city', trip.origin)
                            if arr_info:
                                nome_destino = arr_info[0].get('city', trip.destination)

            except Exception as e:
                print(f"Erro na data {data_ida_atual}: {e}")
                continue 
                
        if voo_escolhido:
            return {
                "success": True,
                "price": melhor_preco_da_janela,
                "airline": voo_escolhido["flights"][0]["airline"],
                "link": link_final,
                "date": data_do_voo_escolhido,
                "origin_name": nome_origem,
                "destination_name": nome_destino,
                "trip": trip
            }
        else:
            return {"success": False, "error": "O Google Flights não encontrou voos para esta janela de datas."}