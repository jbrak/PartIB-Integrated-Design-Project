from machine import Pin
from utime import sleep

red = Pin(10, Pin.OUT)
blue = Pin(11, Pin.OUT)
green = Pin(12, Pin.OUT)
yellow = Pin(14, Pin.OUT)

def turn_off():
    red.value(0)
    blue.value(0)
    green.value(0)
    yellow.value(0)

def show_resistance(resistance):
    match resistance:
        case "100":
            blue.value(1)
        case "1k":
            green.value(1)
        case "10k":
            red.value(1)
        case "100k":
            yellow.value(1)

if __name__ == "__main__":
    while True:
        turn_off()
        red.value(1)
        sleep(1)
        turn_off()
        blue.value(1)
        sleep(1)
        turn_off()
        green.value(1)
        sleep(1)
        turn_off()
        yellow.value(1)
        sleep(1)