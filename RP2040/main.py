import select
import sys
import utime
import machine
import bme280

i2c = machine.I2C(0, freq=399361, scl=machine.Pin(1), sda=machine.Pin(0))


bme = bme280.BME280(i2c=i2c, address=0x76)

while True:
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.readline()
        if ch[0] == "0":
            print(bme.raw_values[0] + " C")
        if ch[0] == "1":
            print(bme.raw_values[1] + " hPa")
        if ch[0] == "2":
            print(bme.raw_values[2] + " %")

    utime.sleep(1)
