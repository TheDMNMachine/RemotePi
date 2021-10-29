import serial
import time

def read_from_sensor(value_code: str) -> float:
    com = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    value_code = bytes((value_code + '\n'), 'UTF-8')
    com.write(value_code)
    if com.inWaiting() > 0:
        response = com.read(com.inWaiting())
        com.close()
    else:
        time.sleep(2)
        response = com.read(com.inWaiting())
        com.close()
    raw = response.decode('utf-8')
    try:
        return float(raw.split(' ')[0])
    except ValueError:
        print("Controller fail")
        pass


if __name__ == "__main__":
    while True:
        code = input('Value: ')
        print(read_from_sensor(code))
