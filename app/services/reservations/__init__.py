from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Session, select
from app.database import get_session
from app.database.models import Reservation, Table, TimeSlot

from datetime import date, time
from sqlalchemy import Date


async def list_reservations(
    session: Session,
    date_filter: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
):
    try:
        stmt = select(Reservation)
        if date_filter:
            stmt = stmt.join(TimeSlot).where(TimeSlot.start_time.cast(Date) == date_filter)
        if status:
            stmt = stmt.where(Reservation.status == status)
        return session.exec(stmt).all()
    except Exception as e:
        print("list_reservations Catch:", e)
        raise

async def create_reservation(res: Reservation, session: Session):
    try:
        db_res = Reservation(**res.dict(exclude_unset=True))
        session.add(db_res)
        session.commit()
        session.refresh(db_res)
        return db_res
    except Exception as e:
        print("create_reservation Catch:", e)
        session.rollback()
        raise

async def get_reservation(id: int, session: Session):
    try:
        stmt = select(Reservation).where(Reservation.id == id)
        res = session.exec(stmt).first()
        if not res:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return res
    except Exception as e:
        print("get_reservation Catch:", e)
        raise

async def update_reservation(id: int, res: Reservation, session: Session):
    try:
        stmt = select(Reservation).where(Reservation.id == id)
        db_res = session.exec(stmt).first()
        if not db_res:
            raise HTTPException(status_code=404, detail="Reservation not found")
        for k, v in res.dict(exclude_unset=True).items():
            setattr(db_res, k, v)
        session.add(db_res)
        session.commit()
        session.refresh(db_res)
        return db_res
    except Exception as e:
        print("update_reservation Catch:", e)
        session.rollback()
        raise

async def delete_reservation(id: int, session: Session):
    try:
        stmt = select(Reservation).where(Reservation.id == id)
        db_res = session.exec(stmt).first()
        if not db_res:
            raise HTTPException(status_code=404, detail="Reservation not found")
        session.delete(db_res)
        session.commit()
        return {"message": f"Reservation {id} cancelled"}
    except Exception as e:
        print("delete_reservation Catch:", e)
        session.rollback()
        raise

async def allocate_table(party_size: int, session: Session):
    try:
        stmt = select(Table).where(
            Table.capacity >= party_size,
            Table.status == "available"
        )
        table = session.exec(stmt).first()
        if not table:
            return {"detail": "No suitable table available"}
        return {"allocated_table": table}
    except Exception as e:
        print("allocate_table Catch:", e)
        raise

async def combine_tables(party_size: int, session: Session):
    try:
        stmt = select(Table).where(
            Table.status == "available"
        )
        available = session.exec(stmt).all()
        selected, total = [], 0
        for t in available:
            selected.append(t)
            total += t.capacity
            if total >= party_size:
                return {"combined_tables": selected}
        return {"detail": "Not enough tables available to combine"}
    except Exception as e:
        print("combine_tables Catch:", e)
        raise

async def check_availability(date: date, start: time, end: time, party_size: int, session: Session):
    try:
        stmt_res = select(Reservation).join(TimeSlot).where(
            TimeSlot.start_time == start,
            TimeSlot.end_time == end,
            TimeSlot.day_of_week == date.weekday(),
            Reservation.status == "active"
        )
        if session.exec(stmt_res).first():
            return {"available": False, "detail": "Slot already booked"}
        stmt_tbl = select(Table).where(
            Table.capacity >= party_size,
            Table.status == "available"
        )
        return {"available": bool(session.exec(stmt_tbl).first())}
    except Exception as e:
        print("check_availability Catch:", e)
        raise
