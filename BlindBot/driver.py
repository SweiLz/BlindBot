import math
import time

import pigpio

from .dcmotor import DCMotor


class Omni3Wheel:
    """
        PinM1 -> (PWM, INA, INB) Motor #1
        PinM2 -> (PWM, INA, INB) Motor #2
        PinM3 -> (PWM, INA, INB) Motor #3
        gain -> (x, x, x) Motor PWM Gain
    """

    def __init__(self, pi, pinM1, pinM2, pinM3, wheel_rad, wheel_sep, gain=(1, 1, 1)):
        self.pi = pi
        _pwmM1, _inAM1, _inBM1 = pinM1
        _pwmM2, _inAM2, _inBM2 = pinM2
        _pwmM3, _inAM3, _inBM3 = pinM3
        self._wheel_radius = wheel_rad
        self._wheel_separate = wheel_sep
        self._gain = gain
        self.motor1 = DCMotor(self.pi, _pwmM1, _inAM1, _inBM1)
        self.motor2 = DCMotor(self.pi, _pwmM2, _inAM2, _inBM2)
        self.motor3 = DCMotor(self.pi, _pwmM3, _inAM3, _inBM3)

    def drive(self, v):
        d = self._wheel_separate
        r = self._wheel_radius
        u = [
            (v[0] * math.sin(math.pi/3) - v[1]/2 - v[2]*d)/r*self._gain[0],
            (v[0] * -math.sin(math.pi/3) - v[1]/2 - v[2]*d)/r*self._gain[1],
            (v[1] - v[2]*d)/r*self._gain[2]
        ]
        self.motor1.setSpeed(u[0])
        self.motor2.setSpeed(u[1])
        self.motor3.setSpeed(u[2])
        return u


# if __name__ == "__main__":
#     pi = pigpio.pi()
#     drive = Omni3Wheel(pi, (13, 6, 5), (19, 26, 21),
#                        (12, 16, 20), 0.05, 0.15, (0.1, 0.1, 0.1))
#     try:
#         while True:
#             u = drive.drive((0, -0.2, 0))
#             time.sleep(3)
#             u = drive.drive((0.2, 0, 0))
#             time.sleep(3)

#     except KeyboardInterrupt:
#         pass
#     finally:
#         drive.drive((0, 0, 0))
#     pi.stop()
