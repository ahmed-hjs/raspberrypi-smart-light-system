import smbus
import time
from led import RGBLed


address = 0x48
bus = smbus.SMBus(1)

def read(channel):
    bus.write_byte(address, 0x40 | channel)
    bus.read_byte(address)
    
    return bus.read_byte(address)


color = 0x000000
led = RGBLed()

try:
    while True:
        led.set_color(color)
        
        light_value = read(1)
        
        r = (color & 0xFF0000) >> 16
        g = (color & 0x00FF00) >> 8
        b = (color & 0x0000FF)

        light_value_r = r + light_value
        light_value_g = g + light_value
        light_value_b = b + light_value
        
        light_value_mapped_r = led.map_(light_value_r,100,435,0,100)
        light_value_mapped_g = led.map_(light_value_g,100,435,0,100)
        light_value_mapped_b = led.map_(light_value_b,100,435,0,100)

        print(light_value, light_value_r,light_value_b,light_value_g)
        
        led.set_brightness(light_value_mapped_r,light_value_mapped_g,light_value_mapped_b)
        
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Exit")
    led.cleanup()
