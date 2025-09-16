from fastapi import APIRouter
from .table_management import router as tables_routes
from .time_slot import router as times_routes
from .reservations import router as reservations_routes
from .customers import router as customers_routes
from .reports import router as reports_routes

router = APIRouter()

router.include_router(tables_routes, prefix="/tables", tags=["tables"])
router.include_router(times_routes, prefix="/timeslots", tags=["time-slot"])
router.include_router(reservations_routes, prefix="/reservations", tags=["reservations"])
router.include_router(customers_routes, prefix="/customers", tags=["customers"])
router.include_router(reports_routes, prefix="/reports", tags=["reports"])