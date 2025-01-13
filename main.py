from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import psycopg2
import os
import requests
import xmltodict
import threading

app = FastAPI()


class Item(BaseModel):
    name: str
    flash_size: int
    cpu_temp: float
    temperature_inside: float
    humidity_inside: float
    temperature_outside: float
    humidity_outside: float
    pressure: float
    temperature_outside2: float


def get_db():
    conn = psycopg2.connect(database="postgres",
                            host=os.environ['POSTGRES_IP'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'],
                            port=int(os.environ['POSTGRES_PORT']))
    return conn.cursor()


def add_weather_outside(item: Item):
    conn = psycopg2.connect(database="postgres",
                            host=os.environ['POSTGRES_IP'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'],
                            port=int(os.environ['POSTGRES_PORT']))
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather_center.outside (device_name, flash_size, cpu_temp, temperature1, temperature2, humidity, pressure)"
        " VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (item.name, item.flash_size, item.cpu_temp, item.temperature_outside, item.temperature_outside2, item.humidity_outside, item.pressure))
    conn.commit()
    conn.close()

def add_weather_inside(item: Item):
    conn = psycopg2.connect(database="postgres",
                            host=os.environ['POSTGRES_IP'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'],
                            port=int(os.environ['POSTGRES_PORT']))
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weather_center.inside (temperature,humidity)"
        " VALUES (%s,%s)",
        (item.temperature_inside, item.humidity_inside))
    conn.commit()
    conn.close()



def cracow_weather():
    response = requests.get("http://meteo2.ftj.agh.edu.pl/meteo/meteo.xml")
    tree = xmltodict.parse(response.content)
    dane = tree['meteo']['dane_aktualne']
    temperature = float(dane['ta'].split(" ")[0])
    humidity = float(dane['ua'].split(" ")[0])
    pressure = float(dane['pa'].split(" ")[0])*100

    conn = psycopg2.connect(database="postgres",
                            host=os.environ['POSTGRES_IP'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PASSWORD'],
                            port=int(os.environ['POSTGRES_PORT']))
    cursor = conn.cursor()
    cursor.execute(
        "insert into weather_center.cracow(temperature, pressure, humidity) VALUES (%s,%s,%s);",
        (temperature, pressure, humidity))
    conn.commit()
    conn.close()
    threading.Timer(60*60, cracow_weather).start()
cracow_weather()


@app.post("/weather_center")
async def weather_center(item: Item):
    print(item)
    add_weather_outside(item)
    add_weather_inside(item)
    return {"message": "ok"}
