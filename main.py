from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rpi_control import turn_off_led, turn_on_led
from pico_control import read_from_sensor
import asyncio

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/status")
async def status():
    return {"message": "work"}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/on")
def turn_on():
    turn_on_led()


@app.get("/off")
def turn_off():
    turn_off_led()

@app.get("/temperature")
def get_temperature():
    temp = read_from_sensor('0')
    return {'temperature': temp}


@app.get("/humidity")
def get_humidity():
    humidity = read_from_sensor('2')
    return {'humidity': humidity}


@app.get("/pressure")
def get_pressure():
    pressure = read_from_sensor('1')
    return {'pressure': pressure}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(10)
        temp = read_from_sensor('0')
        await websocket.send_text(f"Temperature is : {temp}")
        # data = await websocket.receisc2ve_text()
        # if data == "press":
        #     press = read_from_sensor('1')
        #     await websocket.send_text(f"Pressure is : {press}")
        # if data == "hum":
        #     hum = read_from_sensor('2')
        #     await websocket.send_text(f"Humidity is : {hum}")
