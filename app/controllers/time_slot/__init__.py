from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from app.database import get_session
from app.database.models import TimeSlot
from app.services import time_slot as time_slot_services

router = APIRouter()

@router.get("/", response_model=List[TimeSlot])
async def list_timeslots(session: Session = Depends(get_session)):
    try:
        timeslots = await time_slot_services.list_timeslots(session)
        return timeslots
    except Exception as e:
        print("list_timeslots Catch:", e)
        raise

@router.post("/", response_model=TimeSlot)
async def create_timeslot(slot: TimeSlot, session: Session = Depends(get_session)):
    try:
        created_timeslots = await time_slot_services.create_timeslot(slot, session)
        return created_timeslots
    except Exception as e:
        print("create_timeslot Catch:", e)
        session.rollback()
        raise

@router.put("/{id}", response_model=TimeSlot)
async def update_timeslot(id: int, slot: TimeSlot, session: Session = Depends(get_session)):
    try:
        update_timeslot = await time_slot_services.update_timeslot(id, slot, session)
        return update_timeslot
    except Exception as e:
        print("update_timeslot Catch:", e)
        session.rollback()
        raise

@router.delete("/{id}")
async def delete_timeslot(id: int, session: Session = Depends(get_session)):
    try:
        await time_slot_services.delete_timeslot(id, session)
        return {"message": f"Time slot {id} deleted"}
    except Exception as e:
        print("delete_timeslot Catch:", e)
        session.rollback()
        raise
