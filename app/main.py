from fastapi import FastAPI, Query
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
import os

# DATABASE
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Table definition
conversions = Table(
    "conversions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("original_value", Float),
    Column("from_currency", String),
    Column("to_currency", String),
    Column("converted_value", Float),
)

# Create table if not exists
metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine, future=True)

# FastAPI app
app = FastAPI(
    title="API Converter",
    description="API of conversion with Prometheus metrics and persistency",
    version="1.2.0"
)

# Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "API Converter running with persistency!"}

@app.get("/converter")
async def converter(
    value: float = Query(...),
    from_: str = Query(..., alias="from"),
    to: str = Query(...)
):
    # Conversion logic
    rate = 5.0 if from_.lower() == "usd" and to.lower() == "brl" else 1.0
    result = value * rate

    # Insert into database safely
    session = SessionLocal()
    try:
        session.execute(
            conversions.insert().values(
                original_value=value,
                from_currency=from_,
                to_currency=to,
                converted_value=result,
            )
        )
        session.commit()
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()

    return {
        "original_value": value,
        "from_": from_,
        "to": to,
        "converted_value": result
    }

@app.get("/history")
async def history():
    session = SessionLocal()
    try:
        result = session.execute(conversions.select()).all()
    finally:
        session.close()
    return {"history": [dict(r._mapping) for r in result]}