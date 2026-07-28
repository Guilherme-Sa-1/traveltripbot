from sqlalchemy import select
from app.database.database import SessionLocal
from app.database.models import Trip

class TripRepository:
    def save_trip(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: str,
        adults: int,
        budget: float,
    ) -> Trip:
        session = SessionLocal()
        try:
            trip = Trip(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults,
                budget=budget,
            )
            session.add(trip)
            session.commit()
            session.refresh(trip)
            return trip
        finally:
            session.close()

    def get_all_trips(self) -> list[Trip]:
        session = SessionLocal()
        try:
            stmt = select(Trip)
            trips = session.scalars(stmt).all()
            return trips
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