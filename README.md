# Conversor API

API simples de conversão, feita com FastAPI.

## Endpoints
- `/convert/celsius-to-fahrenheit?c=30`
- `/convert/kilometers-to-miles?km=10`

## Rodar localmente
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload