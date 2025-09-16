from fastapi import HTTPException
from sqlmodel import Session, select
from app.database.models import TimeSlot

async def list_timeslots(session: Session):
    try:
        stmt = select(TimeSlot)
        return session.exec(stmt).all()
    except Exception as e:
        print("list_timeslots Catch:", e)
        raise

async def create_timeslot(slot: TimeSlot, session: Session):
    try:
        db_slot = TimeSlot(**slot.dict(exclude_unset=True))
        session.add(db_slot)
        session.commit()
        return db_slot
    except Exception as e:
        print("create_timeslot Catch:", e)
        session.rollback()
        raise

async def update_timeslot(id: int, slot: TimeSlot, session: Session):
    try:
        stmt = select(TimeSlot).where(TimeSlot.id == id)
        db_slot = session.exec(stmt).first()
        if not db_slot:
            raise HTTPException(status_code=404, detail="TimeSlot not found")
        for k, v in slot.dict(exclude_unset=True).items():
            setattr(db_slot, k, v)
        session.add(db_slot)
        session.commit()
        session.refresh(db_slot)
        return db_slot
    except Exception as e:
        print("update_timeslot Catch:", e)
        session.rollback()
        raise

async def delete_timeslot(id: int, session: Session):
    try:
        stmt = select(TimeSlot).where(TimeSlot.id == id)
        db_slot = session.exec(stmt).first()
        if not db_slot:
            raise HTTPException(status_code=404, detail="TimeSlot not found")
        session.delete(db_slot)
        session.commit()
        return {"message": f"Time slot {id} deleted"}
    except Exception as e:
        print("delete_timeslot Catch:", e)
        session.rollback()
        raise
