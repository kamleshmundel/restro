from sqlmodel import Session, select, func
from typing import List
from datetime import date
from app.database.models import Reservation, Table

def daily_report(session: Session):
    try:
        today = date.today()
        today_res: List[Reservation] = session.exec(
            select(Reservation).where(func.date(Reservation.created_at) == today)
        ).all()
        total = len(today_res)
        booked = sum(1 for r in today_res if r.status == "active")
        completed = sum(1 for r in today_res if r.status == "completed")
        cancelled = sum(1 for r in today_res if r.status == "cancelled")
        return {
            "date": today,
            "total_reservations": total,
            "booked": booked,
            "completed": completed,
            "cancelled": cancelled,
            "details": today_res,
        }
    except Exception as e:
        print("daily_report Catch:", e)
        raise

def utilization_report(session: Session):
    try:
        total_tables: int = session.exec(select(func.count(Table.id))).one()
        occupied: int = session.exec(select(func.count(Table.id)).where(Table.status == "occupied")).one()
        available = total_tables - occupied
        utilization_rate = (occupied / total_tables * 100) if total_tables else 0
        return {
            "total_tables": total_tables,
            "occupied_tables": occupied,
            "available_tables": available,
            "utilization_rate": f"{utilization_rate:.2f}%",
        }
    except Exception as e:
        print("utilization_report Catch:", e)
        raise
