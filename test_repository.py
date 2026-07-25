from app.database.repository import TripRepository

repo = TripRepository()

trip = repo.save_trip(
    origin="Fortaleza",
    destination="Tóquio",
    departure_date="15/03/2027",
    return_date="30/03/2027",
    adults=2,
    budget=4500,
)

print("Viagem salva!")

print(f"ID: {trip.id}")
print(f"Destino: {trip.destination}")