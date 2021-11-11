import serial
import time
import tempfile
import json
from datetime import datetime
from enum import Enum


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ValueCodeForSensor(Enum):
    temperature : str = '0'
    pressure : str = '1'
    humidity : str = '2'


class Pico(metaclass=Singleton):
    def __init__(self):
        self.com = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.temp_file = tempfile.TemporaryFile('w+b')

    def read_from_sensor(self, value_code: str) -> float:
        if not self.com.is_open:
            self.com.open()
        value_code = bytes((value_code + '\n'), 'UTF-8')
        self.com.write(value_code)
        if self.com.inWaiting() > 0:
            response = self.com.read(self.com.inWaiting())
            self.com.close()
        else:
            time.sleep(2)
            response = self.com.read(self.com.inWaiting())
            self.com.close()
        raw = response.decode('utf-8')
        try:
            return float(raw.split(' ')[0])
        except ValueError:
            print("Controller fail")
            pass






if __name__ == "__main__":
    pico = Pico()
    pico2 = Pico()
    print(type(pico) == type(pico2))
    while True:
        code = input('Value: ')
        print(pico.read_from_sensor(code))
        time.sleep(3)
        print(pico2.read_from_sensor(code))