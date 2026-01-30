from machine import Pin
import utime

class Button:
    def __init__(self, pin, debounce_ms=200):
        """Initialize button on specified pin with pull-down resistor."""
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.toggle = 0
        self.debounce_ms = debounce_ms

        self.pin.irq(trigger=Pin.IRQ_RISING, handler=self.handler)

        self.last_pressed = utime.ticks_ms()


    def handler(self, pin):
        """Interrupt handler for button press."""
        now = utime.ticks_ms()

        if utime.ticks_diff(now, self.last_pressed) > self.debounce_ms:
            self.toggle += 1
            self.last_pressed = now


    def value(self):
        """Return the current value of the button pin."""
        return self.pin.value()