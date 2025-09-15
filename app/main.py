from fastapi import FastAPI

app = FastAPI(title="Conversor API", version="1.0.0")

@app.get("/convert/celsius-to-fahrenheit")
def celsius_to_fahrenheit(c: float):
    """Converte Celsius para Fahrenheit"""
    f = (c * 9/5) + 32
    return {"celsius": c, "fahrenheit": f}

@app.get("/convert/kilometers-to-miles")
def kilometers_to_miles(km: float):
    """Converte quilômetros para milhas"""
    miles = km * 0.621371
    return {"kilometers": km, "miles": miles}
