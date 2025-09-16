from fastapi import HTTPException
from sqlmodel import Session, select
from app.database.models import Customer, Reservation

async def list_customers(session: Session):
    try:
        stmt = (select(Customer))
        result = session.exec(stmt)
        customers = result.all()

        return customers
    except Exception as e:
        print("modality_details Catch:", e)
        raise

async def create_customer(cust: Customer, session: Session):
    try:
        db_cust = Customer(**cust.dict())
        session.add(db_cust)
        session.commit()
        return db_cust
    except Exception as e:
        print("create_customer Catch:", e)
        session.rollback()
        raise

async def get_customer(id: int, session: Session):
    try:
        stmt = select(Customer).where(Customer.id == id)
        result = session.exec(stmt).first()
        if not result:
            raise HTTPException(status_code=404, detail="Customer not found")
        return result
    except Exception as e:
        print("get_customer Catch:", e)
        raise


async def update_customer(id: int, cust: Customer, session: Session):
    try:
        stmt = select(Customer).where(Customer.id == id)
        db_cust = session.exec(stmt).first()
        if not db_cust:
            raise HTTPException(status_code=404, detail="Customer not found")
        for k, v in cust.dict(exclude_unset=True).items():
            setattr(db_cust, k, v)
        session.add(db_cust)
        session.commit()
        return db_cust
    except Exception as e:
        print("update_customer Catch:", e)
        session.rollback()
        raise


async def customer_history(id: int, session: Session):
    try:
        stmt = select(Reservation).where(Reservation.customer_id == id)
        result = session.exec(stmt).all()
        return result
    except Exception as e:
        print("customer_history Catch:", e)
        raise
