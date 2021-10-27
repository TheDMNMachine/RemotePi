import serial
import time

async def  read_from_sensor(value_code):
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
    return float(raw.split(' ')[0])

if __name__ == "__main__":
    while True:
        code = input('Value: ')
        print(read_from_sensor(code))
