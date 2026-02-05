from machine import Pin, PWM

class Motor:
    def __init__(self, dirPin, PWMPin,drift_compensation=0):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        self.drift_compensation = drift_compensation
        self.offset = 0

    def off(self):
        self.pwm.duty_u16(0)

    def forward(self, speed=100, offset=0):
        self.mDir.value(0)  # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * (speed-self.drift_compensation-offset) / 100))  # speed range 0-100 motor

    def reverse(self, speed=30, offset=0):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * (speed-self.drift_compensation-offset) / 100))

class Motors:
    '''Dual motor driver class for controlling port and starboard motors.'''
    def __init__(self, pDIR, pPWM, sDIR, sPWM, pdrift_compensation=0, sdrift_compensation=0):
        '''Initialize dual motors with specified direction and PWM pins.'''
        self.p = Motor(dirPin= pDIR, PWMPin = pPWM, drift_compensation= pdrift_compensation)
        self.s = Motor(dirPin= sDIR, PWMPin = sPWM, drift_compensation=sdrift_compensation)

    def off(self):
        self.p.off()
        self.s.off()

    def forward(self, speed=100):
        self.p.forward(speed)
        self.s.forward(speed)

    def reverse(self, speed=30):
        self.p.reverse(speed)
        self.s.reverse(speed)

if __name__ == "__main__":
    motors = Motors(pDIR=4, pPWM=5, sDIR=7, sPWM=6, pdrift_compensation=0, sdrift_compensation=0)
    try:
        while True:
            speed = int(input("Enter speed: "))

            motors.forward(speed)
    except KeyboardInterrupt:
        motors.off()