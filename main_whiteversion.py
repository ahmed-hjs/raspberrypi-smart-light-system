import smbus
import time
from led import RGBLed


address = 0x48
bus = smbus.SMBus(1)

def read(channel):
    bus.write_byte(address, 0x40 | channel)
    bus.read_byte(address)
    
    return bus.read_byte(address)

led = RGBLed()

try:
    while True: 
        light_value = read(1)
        light_value_mapped = led.map_(light_value,80,180,0,100)
        led.set_brightness(light_value_mapped,light_value_mapped,light_value_mapped)
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Exit")
    led.cleanup()
