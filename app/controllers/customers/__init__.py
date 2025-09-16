from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from app.database import get_session
from app.database.models import Customer, Reservation
from app.services import customers as customers_services

router = APIRouter()

@router.get("/", response_model=List[Customer])
async def list_customers(session: Session = Depends(get_session)):
    try:
        customers = await customers_services.list_customers(session)
        return customers
    except Exception as e:
        print("modality_details Catch:", e)
        raise

@router.post("/", response_model=Customer)
async def create_customer(cust: Customer, session: Session = Depends(get_session)):
    try:
        created_cust = await customers_services.create_customer(cust, session)
        return created_cust
    except Exception as e:
        print("create_customer Catch:", e)
        raise

@router.get("/{id}", response_model=Customer)
async def get_customer(id: int, session: Session = Depends(get_session)):
    try:
        customer = await customers_services.get_customer(id, session)
        return customer
    except Exception as e:
        print("get_customer Catch:", e)
        raise


@router.put("/{id}", response_model=Customer)
async def update_customer(id: int, cust: Customer, session: Session = Depends(get_session)):
    try:
        updated_cust = await customers_services.update_customer(id, cust, session)
        return updated_cust
    except Exception as e:
        print("update_customer Catch:", e)
        raise


@router.get("/{id}/history", response_model=List[Reservation])
async def customer_history(id: int, session: Session = Depends(get_session)):
    try:
        history = await customers_services.customer_history(id, session)
        return history
    except Exception as e:
        print("customer_history Catch:", e)
        raise
