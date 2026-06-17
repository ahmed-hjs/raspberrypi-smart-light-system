import RPi.GPIO as GPIO


class RGBLed:
    def __init__(self, pin_r=17, pin_g=18, pin_b=27, frequency=2000):
        self.pins = {
            "pin_R": pin_r,
            "pin_G": pin_g,
            "pin_B": pin_b,
        }

        GPIO.setmode(GPIO.BCM)

        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)  # Common-anode RGB LED OFF

        self.p_R = GPIO.PWM(self.pins["pin_R"], frequency)
        self.p_G = GPIO.PWM(self.pins["pin_G"], frequency)
        self.p_B = GPIO.PWM(self.pins["pin_B"], frequency)

        self.p_R.start(0)
        self.p_G.start(0)
        self.p_B.start(0)


    def map_(self,x, in_min, in_max, out_min, out_max):
        value = out_max - ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        if value < out_min :
            return out_min
        if value > out_max:
            return out_max - 0.1
        else:
            return value

    def set_color(self, color):

        r = (color & 0xFF0000) >> 16
        g = (color & 0x00FF00) >> 8
        b = (color & 0x0000FF)

        r = self.map_(r,0, 255, 0, 100)
        g = self.map_(g,0, 255, 0, 100)
        b = self.map_(b,0, 255, 0, 100)

        self.p_R.ChangeDutyCycle(r)
        self.p_G.ChangeDutyCycle(g)
        self.p_B.ChangeDutyCycle(b)
        return r,g,b


    def set_brightness(self,r,g,b):
        self.p_R.ChangeDutyCycle(r)
        self.p_G.ChangeDutyCycle(g)
        self.p_B.ChangeDutyCycle(b)
        
    def off(self):
        for pin in self.pins.values():
            GPIO.output(pin, GPIO.HIGH)

    def cleanup(self):
        self.p_R.stop()
        self.p_G.stop()
        self.p_B.stop()

        self.off()
        GPIO.cleanup()