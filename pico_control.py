import serial
import time
from enum import Enum

class ValueCodeForSensor(Enum):
    temperature = '0'
    pressure = '1'
    humidity = '2'


class Pico:
    def __init__(self):
        self.com = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

    def read_from_sensor(self, value_code: str) -> float:
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
    while True:
        code = input('Value: ')
        pico = Pico()
        print(pico.read_from_sensor(code))