from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    departure_date = Column(String)
    return_date = Column(String)
    adults = Column(Integer)
    budget = Column(Float)
    
    # Coluna adicionada para o sistema anti-spam do despertador
    last_notified_price = Column(Float, nullable=True)