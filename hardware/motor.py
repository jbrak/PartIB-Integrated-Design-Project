from machine import Pin, PWM

class Motor:
    """
    The object holding one motor
    
    Attributes
    ----------
    mDir : Pin
        Holds the direction pin for the motor
    pwm : PWM
        Holds the PWM for the motor
    drift_compensation : int
        Holds the factor that we need to account for drift compensation when setting speed
    offset : int
        Holds the offset for speed

    Methods
    -------
    off()
    forward(speed=100, offset=0)
    reverse(speed=30, offset=0)
    """

    def __init__(self, dirPin, PWMPin,drift_compensation=0):
        """
        Initialize a motors with specified direction and PWM pins.
        
        Parameters
        ----------
        dirPin : int
            The motor's direction pin 
        PWMPin : int
            The notor's PWM pin
        drift_compensation : int, optional
            The drift compensation for the motor (Default = 0)
        """

        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        self.drift_compensation = drift_compensation
        self.offset = 0

    def off(self):
        """Turns the motor off"""
        self.pwm.duty_u16(0)

    def forward(self, speed=100, offset=0):
        """
        Rotates motor in the forward direction
        
        Parameters
        ----------
        speed : int, optional
            Sets the speed of the motor (Default = 100)
        offset : int, optional
            Offsets the speed of the motor (Default = 0)
        """
        self.mDir.value(0)  # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * (speed-self.drift_compensation*(speed/100)-offset) / 100))  # speed range 0-100 motor

    def reverse(self, speed=30, offset=0):
        """
        Rotates motor in the reverse direction
        
        Parameters
        ----------
        speed : int, optional
            Sets the speed of the motor (Default = 30)
        offset : int, optional
            Offsets the speed of the motor (Default = 0)
        """

        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * (speed-self.drift_compensation*(speed/100)-offset) / 100))

class Motors:
    """
    Dual motor driver class for controlling port and starboard motors.
    
    Attributes
    ----------
    p : Motor
        Holds the port motor
    s : Motor
        Holds the starboard motor

    Methods
    -------
    off()
    forward(speed=100)
    reverse(speed=30)
    """

    def __init__(self, pDIR, pPWM, sDIR, sPWM, pdrift_compensation=0, sdrift_compensation=0):
        """
        Initialize dual motors with specified direction and PWM pins.
        
        Parameters
        ----------
        pDIR : int
            The port motor's direction pin 
        pPWM : int
            The port notor's PWM pin 
        sDIR : int
            The starboard motor's direction pin 
        sPWM : int
            The starboard motor's PWM pin 
        pdrift_compensation : int, optional
            The drift compensation for the port motor (Default = 0)
        sdrift_compensation : int, optional
            The drift compensation for the starboard motor (Default = 0)
        """

        self.p = Motor(dirPin= pDIR, PWMPin = pPWM, drift_compensation=pdrift_compensation)
        self.s = Motor(dirPin= sDIR, PWMPin = sPWM, drift_compensation=sdrift_compensation)

    def off(self):
        """Turns both motors off"""
        self.p.off()
        self.s.off()

    def forward(self, speed=100):
        """
        Rotates motor in the forward direction
        
        Parameters
        ----------
        speed : int, optional
            Sets the speed of the motor (Default = 100)
        """
        self.p.forward(speed)
        self.s.forward(speed)

    def reverse(self, speed=30):
        """
        Rotates motor in the reverse direction
        
        Parameters
        ----------
        speed : int, optional
            Sets the speed of the motor (Default = 30)
        """
        self.p.reverse(speed)
        self.s.reverse(speed)

if __name__ == "__main__":
    """Test code for the motors"""
    motors = Motors(pDIR=4, pPWM=5, sDIR=7, sPWM=6, pdrift_compensation=0, sdrift_compensation=0)
    try:
        while True:
            speed = int(input("Enter speed: "))

            motors.forward(speed)
    except KeyboardInterrupt:
        motors.off()