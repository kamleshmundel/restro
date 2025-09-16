from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from sqlmodel import Session
from app.database import get_session
from app.database.models import Reservation
from app.services import reservations as reservations_services
from datetime import date, time

router = APIRouter()

@router.get("/", response_model=List[Reservation])
async def list_reservations(
    date_filter: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    try:
        reservations = await reservations_services.list_reservations(session, date_filter, status)
        return reservations
    except Exception as e:
        print("list_reservations Catch:", e)
        raise

@router.post("/", response_model=Reservation)
async def create_reservation(res: Reservation, session: Session = Depends(get_session)):
    try:
        created_res = await reservations_services.create_reservation(res, session)
        return created_res
    except Exception as e:
        print("create_reservation Catch:", e)
        raise

@router.get("/{id}", response_model=Reservation)
async def get_reservation(id: int, session: Session = Depends(get_session)):
    try:
        reservation = await reservations_services.get_reservation(id, session)
        return reservation
    except Exception as e:
        print("get_reservation Catch:", e)
        raise

@router.put("/{id}", response_model=Reservation)
async def update_reservation(id: int, res: Reservation, session: Session = Depends(get_session)):
    try:
        updated_res = await reservations_services.update_reservation(id, res, session)
        return updated_res
    except Exception as e:
        print("update_reservation Catch:", e)
        raise

@router.delete("/{id}")
async def delete_reservation(id: int, session: Session = Depends(get_session)):
    try:
        await reservations_services.delete_reservation(id, session)
        return {"message": f"Reservation {id} cancelled"}
    except Exception as e:
        print("delete_reservation Catch:", e)
        raise

@router.post("/allocate")
async def allocate_table(party_size: int, session: Session = Depends(get_session)):
    try:
        allocation = await reservations_services.allocate_table(party_size, session)
        return allocation
    except Exception as e:
        print("allocate_table Catch:", e)
        raise

@router.post("/combine")
async def combine_tables(party_size: int, session: Session = Depends(get_session)):
    try:
        combine = await reservations_services.combine_tables(party_size, session)
        return combine
    except Exception as e:
        print("combine_tables Catch:", e)
        raise

@router.get("/check")
async def check_availability(date: date, start: time, end: time, party_size: int, session: Session = Depends(get_session)):
    try:
        availability = await reservations_services.check_availability(date, start, end, party_size, session)
        return availability
    except Exception as e:
        print("check_availability Catch:", e)
        raise
