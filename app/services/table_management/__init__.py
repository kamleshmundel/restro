from fastapi import HTTPException
from app.database.models import Table
from sqlmodel import Session, select

async def list_tables(session: Session):
    try:
        return session.exec(select(Table)).all()
    except Exception as e:
        print("list_tables Catch:", e)
        raise

async def create_table(table: Table, session: Session):
    try:
        db_table = Table(**table.dict(exclude_unset=True))
        session.add(db_table)
        session.commit()
        return db_table
    except Exception as e:
        print("create_table Catch:", e)
        session.rollback()
        raise

async def get_table(id: int, session: Session):
    try:
        table = session.exec(select(Table).where(Table.id == id)).first()
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        return table
    except Exception as e:
        print("get_table Catch:", e)
        raise

async def update_table(id: int, table: Table, session: Session):
    try:
        db_table = session.exec(select(Table).where(Table.id == id)).first()
        if not db_table:
            raise HTTPException(status_code=404, detail="Table not found")
        for k, v in table.dict(exclude_unset=True).items():
            setattr(db_table, k, v)
        session.add(db_table)
        session.commit()
        return db_table
    except Exception as e:
        print("update_table Catch:", e)
        session.rollback()
        raise

async def delete_table(id: int, session: Session):
    try:
        db_table = session.exec(select(Table).where(Table.id == id)).first()
        if not db_table:
            raise HTTPException(status_code=404, detail="Table not found")
        session.delete(db_table)
        session.commit()
        return {"message": f"Table {id} deleted"}
    except Exception as e:
        print("delete_table Catch:", e)
        session.rollback()
        raise