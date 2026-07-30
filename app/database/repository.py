from app.database.database import SessionLocal
from app.database.models import Trip

class TripRepository:
    def add_trip(self, origin: str, destination: str, departure_date: str, return_date: str, adults: int, budget: float) -> Trip:
        session = SessionLocal()
        try:
            new_trip = Trip(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults,
                budget=budget
            )
            session.add(new_trip)
            session.commit()
            session.refresh(new_trip)
            return new_trip
        finally:
            session.close()

    def get_all_trips(self) -> list[Trip]:
        session = SessionLocal()
        try:
            return session.query(Trip).all()
        finally:
            session.close()

    def get_trip_by_id(self, trip_id: int) -> Trip | None:
        session = SessionLocal()
        try:
            return session.get(Trip, trip_id)
        finally:
            session.close()

    def delete_trip(self, trip_id: int) -> bool:
        session = SessionLocal()
        try:
            trip = session.get(Trip, trip_id)
            if trip:
                session.delete(trip)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def update_budget(self, trip_id: int, new_budget: float) -> bool:
        session = SessionLocal()
        try:
            trip = session.get(Trip, trip_id)
            if trip:
                trip.budget = new_budget
                session.commit()
                return True
            return False
        finally:
            session.close()

    def update_last_notified_price(self, trip_id: int, price: float) -> bool:
        session = SessionLocal()
        try:
            trip = session.get(Trip, trip_id)
            if trip:
                trip.last_notified_price = price
                session.commit()
                return True
            return False
        finally:
            session.close()