# from machine import Pin
# from utime import sleep
#
# #Set the button pin
# button_pin = 22
# button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
#
# def button_handler(pin):
#     print("Button pressed! Interrupt triggered.")
#     sleep(1)
#
# button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
#
# #Continiously update the LED value and print said value
# while True:
#   print(button.value())
#   sleep(0.1)

from hardware.button import Button
from utime import sleep

button = Button(pin=0)

while True:
    print(button.value(), button.toggle)
    sleep(0.1)