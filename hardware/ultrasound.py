from machine import Pin, ADC
from utime import sleep

class Ultrasound:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))

    def read(self):
        return self.adc.read_u16()

if __name__ == "__main__":
    ultrasound = Ultrasound(pin=26)
    try:
        while True:
            distance = ultrasound.read()
            print("Distance:", distance)
            sleep(1)
    except KeyboardInterrupt:
        pass
