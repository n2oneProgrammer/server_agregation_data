from pydantic import BaseModel
import requests
import xmltodict
import threading
import postgres


class WeatherData(BaseModel):
    name: str
    flash_size: int
    cpu_temp: float
    temperature_inside: float
    humidity_inside: float
    temperature_outside: float
    humidity_outside: float
    pressure: float
    temperature_outside2: float


def add_weather_outside(item: WeatherData):
    postgres.push_command(
        "INSERT INTO weather_center.outside (device_name, flash_size, cpu_temp, temperature1, temperature2, humidity, pressure)"
        " VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (item.name, item.flash_size, item.cpu_temp, item.temperature_outside, item.temperature_outside2,
         item.humidity_outside, item.pressure))


def add_weather_inside(item: WeatherData):
    postgres.push_command(
        "INSERT INTO weather_center.inside (temperature,humidity)"
        " VALUES (%s,%s)",
        (item.temperature_inside, item.humidity_inside))


def cracow_weather():
    response = requests.get("http://meteo2.ftj.agh.edu.pl/meteo/meteo.xml")
    tree = xmltodict.parse(response.content)
    dane = tree['meteo']['dane_aktualne']
    temperature = float(dane['ta'].split(" ")[0])
    humidity = float(dane['ua'].split(" ")[0])
    pressure = float(dane['pa'].split(" ")[0]) * 100

    postgres.push_command(
        "insert into weather_center.cracow(temperature, pressure, humidity) VALUES (%s,%s,%s);",
        (temperature, pressure, humidity))

    threading.Timer(60 * 60, cracow_weather).start()


cracow_weather()
