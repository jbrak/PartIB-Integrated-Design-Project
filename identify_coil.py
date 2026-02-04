from machine import Pin
from utime import sleep
import grabber as gb
import find_resistance as fr
import led_board as leds

# Full code to grab a resistor, identify the resistor and lift it

# Grabs the resistor
gb.grab()
sleep(0.5)

# Keeps trying to find the resistance of it until it gets one 
retry = True
resistance = ""
while retry:
    resistance = fr.find_resistance()
    if resistance in ["100", "1k", "10k", "100k"]:
        retry = False
sleep(0.5)

# Shows the LED corresponding to the resistance found in the previous section
leds.show_resistance(resistance)

# Lifts the resistor
gb.lift()