from datetime import datetime, time, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str = Field(unique=True, index=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    dietary_preferences: Optional[str] = None
    special_occasions: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    reservations: List["Reservation"] = Relationship(back_populates="customer")
    visits: List["VisitHistory"] = Relationship(back_populates="customer")


class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    capacity: int
    location: Optional[str] = None
    status: str = Field(default="available")

    reservations: List["ReservationTable"] = Relationship(back_populates="table")


class TimeSlot(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: time
    end_time: time
    day_of_week: int

    reservations: List["Reservation"] = Relationship(back_populates="timeslot")


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    timeslot_id: int = Field(foreign_key="timeslot.id")
    party_size: int
    status: str = Field(default="active")
    preferences: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Customer = Relationship(back_populates="reservations")
    timeslot: TimeSlot = Relationship(back_populates="reservations")
    tables: List["ReservationTable"] = Relationship(back_populates="reservation")
    visits: List["VisitHistory"] = Relationship(back_populates="reservation")


class ReservationTable(SQLModel, table=True):
    reservation_id: int = Field(foreign_key="reservation.id", primary_key=True)
    table_id: int = Field(foreign_key="table.id", primary_key=True)

    reservation: Reservation = Relationship(back_populates="tables")
    table: Table = Relationship(back_populates="reservations")


class VisitHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    reservation_id: int = Field(foreign_key="reservation.id")
    visit_date: date
    notes: Optional[str] = None

    customer: Customer = Relationship(back_populates="visits")
    reservation: Reservation = Relationship(back_populates="visits")


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_date: date = Field(unique=True, index=True)
    total_reservations: int
    occupancy_rate: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
