from machine import Pin
import utime

class Button:
    """
    Class for the start/stop button
    
    Attributes
    ----------
    pin : Pin
        Holds the GPIO pin that the button is connected to
    toggle : int
        Holds the state of the button
    debounce_ms : int
        Holds the button's debounce in milliseconds
    last_pressed : int
        Holds the time since the button was last pressed

    Methods
    -------
    handler(pin)
    value() -> int
    """

    def __init__(self, pin, debounce_ms=200):
        """
        Initialize button on specified pin with pull-down resistor.
        
        Parameters
        ----------
        pin : int
            The pin that the button is connected to
        debounce_ms : int, optional
            The debounce time for the button in milliseconds (Default = 200)
        """

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