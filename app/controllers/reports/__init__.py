from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.services import reports as reports_services

router = APIRouter()

@router.get("/daily")
async def daily_report(session: Session = Depends(get_session)):
    try:
        report = await reports_services.daily_report(session)
        return report
    except Exception as e:
        print("daily_report Catch:", e)
        raise

@router.get("/utilization")
async def utilization_report(session: Session = Depends(get_session)):
    try:
        report = await reports_services.utilization_report(session)
        return report
    except Exception as e:
        print("utilization_report Catch:", e)
        raise