from machine import Pin, ADC
from utime import sleep


class Ultrasound:
    """
    Object for the ultrasound sensor
    
    Attributes
    ----------
    adc : ADC
        Holds the ADC
    
    Methods
    -------
    read() -> int
    """

    def __init__(self, pin):
        """Initialises the ADC"""
        self.adc = ADC(Pin(pin))

    def read(self):
        """Reads the ADC"""
        return self.adc.read_u16()

if __name__ == "__main__":
    """Test code for the ultrasound sensor"""
    ultrasound = Ultrasound(pin=26)
    try:
        while True:
            distance = ultrasound.read()
            print("Distance:", distance)
            sleep(1)
    except KeyboardInterrupt:
        pass
