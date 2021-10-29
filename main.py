from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rpi_control import turn_off_led, turn_on_led
from pico_control import read_from_sensor
import asyncio


description = """
    RemoteRPi API
    Give you access to Raspberry Pi hardware remotely
    """

tags_metadata = [
    {
        "name": "status",
        "description": "Provide information about status of api on current RPi",
    },
    {
        "name": "root",
        "description": "Generate basic web for testing hardware functionality",
        # "externalDocs": {
        #     "description": "external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
    {
        "name": 'on',
        "description": "Turning on LED attached to GPIO21 on Raspberry 3B+"
    },
    {
        "name": 'off',
        "description": "Turning off LED attached to GPIO21 on Raspberry 3B+"
    },
    {
        "name": 'temperature',
        "description": "Provide information about temperature from RP2040 and BME280"
    },
    {
        "name": 'humidity',
        "description": "Provide information about humidity from RP2040 and BME280"
    },
    {
        "name": 'pressure',
        "description": "Provide information about pressure from RP2040 and BME280"
    },
    {
        "name": 'ws',
        "description": "Give acces to websocket that send you current temperature every 30sec"
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="RemotePi API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Damian Jarominek",
        "url": "https://github.com/TheDMNMachine",
        "email": "damian.jarominek@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT.html",
    },
)


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/status", tags=['status'])
async def status():
    return {"message": "work"}


@app.get("/", response_class=HTMLResponse, tags=['root'])
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/on", tags=['on'])
def turn_on():
    turn_on_led()
    return {'status': 'OK'}


@app.get("/off", tags=['off'])
def turn_off():
    turn_off_led()
    return {'status': 'OK'}

@app.get("/temperature", tags=['temperature'])
def get_temperature():
    temp :float = read_from_sensor('0')
    return {'temperature': temp}


@app.get("/humidity", tags=['humidity'])
def get_humidity():
    humidity :float = read_from_sensor('2')
    return {'humidity': humidity}


@app.get("/pressure", tags=['pressure'])
def get_pressure():
    pressure : float = read_from_sensor('1')
    return {'pressure': pressure}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(10)
        temp = read_from_sensor('0')
        await websocket.send_text(f"Temperature is : {temp}")

