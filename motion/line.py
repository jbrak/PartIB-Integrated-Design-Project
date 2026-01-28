from hardware.line import LineSensorArray, LineSensorArrayAlt
from hardware.motor import Motors
from time import sleep

def check_straight_line(motors:Motors, line_sensors: LineSensorArray, t, sensitivity=10):
    """Drive straight while both outer line sensors detect the line."""
    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    if (p, cp, cs, s) == (0, 1, 1, 0):
        print(f'{t}: Continuing straight line')

    elif (cp == 1 and cs == 1 and (p == 1 or s == 1)):
        print(f'{t}: Reached node, stopping')
        motors.off()

    elif (cp == 0 and cs == 0):
        print(f'{t}: Lost line, stopping')
        motors.off()

    elif (p, cp, cs, s) == (0, 0, 1, 0):
        print(f'{t}: Port side lost line, attempting to correct')
        motors.off()
        # motors.p.forward(speed=100)
        # motors.s.forward(speed=100-sensitivity)
        # sleep(0.1)
        # motors.forward(speed=100)

    elif (p, cp, cs, s) == (0, 1, 0, 0):
        print(f'{t}: Starboard side lost line, attempting to correct')
        motors.off()
        # motors.p.forward(speed=100-sensitivity)
        # motors.s.forward(speed=100)
        # sleep(0.1)
        # motors.forward(speed=100)


def check_straight_line_alt(motors:Motors, line_sensors: LineSensorArrayAlt, t):
    """Drive straight while both outer line sensors detect the line."""
    line_data = line_sensors.read_all()

    p = line_data.get('p')
    f = line_data.get('f')
    b = line_data.get('b')
    s = line_data.get('s')

    if (p, f, b, s) == (0, 1, 1, 0):
        print(f'{t}: Continuing straight line')

    elif (b == 1 and (p == 1 or s == 1)):
        print(f'{t}: Reached node, stopping')
        motors.off()

    elif (f == 0 and b == 0):
        print(f'{t}: Lost line, stopping')
        motors.off()

    elif (f, s) == (0, 1):
        print(f'{t}: Port side lost line, attempting to correct')
        motors.off()
        # motors.p.forward(speed=100)
        # motors.s.forward(speed=90)
        # sleep(0.1)
        # motors.forward(speed=100)

    elif (f,p) == (0,1):
        print(f'{t}: Starboard side lost line, attempting to correct')
        motors.off()
        # motors.p.forward(speed=90)
        # motors.s.forward(speed=100)
        # sleep(0.1)
        # motors.forward(speed=100)