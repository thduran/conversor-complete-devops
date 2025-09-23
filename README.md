# Conversor API

Conversion simple API, made withFastAPI.

## Endpoints
- `/convert/celsius-to-fahrenheit?c=30`
- `/convert/kilometers-to-miles?km=10`

## Rodar localmente
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload