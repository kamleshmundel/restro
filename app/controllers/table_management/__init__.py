from fastapi import APIRouter, Depends
from typing import List
from app.database.models import Table
from sqlmodel import Session
from app.database import get_session
from app.services import table_management as table_management_services

router = APIRouter()

@router.get("/", response_model=List[Table])
async def list_tables(session: Session = Depends(get_session)):
    try:
        tables = await table_management_services.list_tables(session)
        return tables
    except Exception as e:
        print("list_tables Catch:", e)
        raise

@router.post("/", response_model=Table)
async def create_table(table: Table, session: Session = Depends(get_session)):
    try:
        created_table = await table_management_services.create_table(table, session)
        return created_table
    except Exception as e:
        print("create_table Catch:", e)
        raise

@router.get("/{id}", response_model=Table)
async def get_table(id: int, session: Session = Depends(get_session)):
    try:
        single_table = await table_management_services.get_table(id, session)
        return single_table
    except Exception as e:
        print("get_table Catch:", e)
        raise

@router.put("/{id}", response_model=Table)
async def update_table(id: int, table: Table, session: Session = Depends(get_session)):
    try:
        updated_table = await table_management_services.update_table(id, table, session)
        return updated_table
    except Exception as e:
        print("update_table Catch:", e)
        raise

@router.delete("/{id}")
async def delete_table(id: int, session: Session = Depends(get_session)):
    try:
        await table_management_services.delete_table(id, session)
        return {"message": f"Table {id} deleted"}
    except Exception as e:
        print("delete_table Catch:", e)
        session.rollback()
        raise