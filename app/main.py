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
    Column("valor_original", Float),
    Column("de_moeda", String),
    Column("para_moeda", String),
    Column("valor_convertido", Float),
)

# it creates the table if not existent
metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

# Initializes API
app = FastAPI(
    title="Conversor API",
    description="API de conversão com métricas Prometheus e persistência",
    version="1.1.0"
)

# Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "API Conversor rodando com persistência!"}

@app.get("/conversor")
async def conversor(
    valor: float = Query(...),
    de: str = Query(...),
    para: str = Query(...)
):
    taxa = 5.0 if de == "usd" and para == "brl" else 1.0
    resultado = valor * taxa

    # Add info to database
    session = SessionLocal()
    session.execute(
        conversions.insert().values(
            valor_original=valor,
            de_moeda=de,
            para_moeda=para,
            valor_convertido=resultado,
        )
    )
    session.commit()
    session.close()

    return {
        "valor_original": valor,
        "de": de,
        "para": para,
        "valor_convertido": resultado
    }

@app.get("/historico")
async def historico():
    session = SessionLocal()
    result = session.execute(conversions.select()).fetchall()
    session.close()
    return {"historico": [dict(r._mapping) for r in result]}