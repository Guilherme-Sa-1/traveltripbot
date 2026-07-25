from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    origin: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    destination: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    departure_date: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    return_date: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    adults: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    budget: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )