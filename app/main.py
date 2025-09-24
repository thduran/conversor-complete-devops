from fastapi import FastAPI, Query
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker
import os

# database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# conversions table definition
conversions = Table(
    "conversions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("original_value", Float),
    Column("from_currency", String),
    Column("to_currency", String),
    Column("converted_value", Float),
)

# it creates the table if not existent
metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

# Initializes API
app = FastAPI(
    title="API Converter",
    description="API of conversion with Prometheus metrics and persistency",
    version="1.1.0"
)

# Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "API Converter running with persistency!"}

@app.get("/converter")
async def converter(
    value: float = Query(...),
    from_: str = Query(...),
    to: str = Query(...)
):
    rate = 5.0 if from_ == "usd" and to == "brl" else 1.0
    result = value * rate

    # Add info to database
    session = SessionLocal()
    session.execute(
        conversions.insert().values(
            original_value=value,
            from_currency=from_,
            to_currency=to,
            converted_value=result,
        )
    )
    session.commit()
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
    result = session.execute(conversions.select()).fetchall()
    session.close()
    return {"history": [dict(r._mapping) for r in result]}