from machine import Pin, ADC
from utime import sleep

""""Returns the value of the resistor between the grabber using the u16 number found by the ADC"""
def find_resistor(voltage) -> str:
    # Values look arbitrary but were tested for the pico
    if voltage < 4000:
        return "100"
    elif voltage < 10000:
        return "1k"
    elif voltage < 40000:
        return "10k"
    elif voltage < 44000:
        return "100k"
    else: return "No Resistor"

"""
Code to figure out resistor.
Works by averaging out the u16 voltage in the ADC and finding the resistance that it corresponds to
"""
def find_resistance(): 
    adc = ADC(Pin(28)) # creates an ADC on GPIO 28 (pin 34)
    voltages = []
    
    for i in range(20): # Reads 100 u16 values through the ADC and adds them all to the voltages array
        voltage = adc.read_u16()
        voltages.append(voltage)
        sleep(0.01)
    
    # Takes the average value of all of the u16 values
    avg = 0
    for i in range(20):
        avg = avg + voltages[i]
    avg = avg / 20
    
    # Uses find_resistor(voltage) to find the resistance needed, and prints it
    resistance = find_resistor(avg)
    print(resistance)
    return resistance

if __name__ == "__main__":
    # Keep looking for the resistance between the grabbers 
    for _ in range(100):
        find_resistance()
        sleep(0.1)