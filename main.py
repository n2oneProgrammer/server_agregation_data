from fastapi import FastAPI
from weather import *

app = FastAPI()


@app.post("/weather_center")
async def weather_center(item: WeatherData):
    print(item)
    add_weather_outside(item)
    add_weather_inside(item)
    return {"message": "ok"}
