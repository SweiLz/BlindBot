import RPi.GPIO as GPIO
from time import sleep
from math import sin, pi
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class DCMotor:
    FREE = 0x00
    BREAK = 0x01
    FORWARD = 0x02
    BACKWARD = 0x03

    def __init__(self, pwm, inA, inB):
        self._pwm_pin = pwm
        self._inA_pin = inA
        self._inB_pin = inB

        GPIO.setup(self._pwm_pin, GPIO.OUT)
        GPIO.setup(self._inA_pin, GPIO.OUT)
        GPIO.setup(self._inB_pin, GPIO.OUT)

        # self._pwm = GPIO.PWM(self._pwm_pin, 100)
        # self._pwm.start(0)
        GPIO.output(self._inA_pin, GPIO.LOW)
        GPIO.output(self._inB_pin, GPIO.LOW)
        self.state = 0

    def setDuty(self, duty):
        if duty > 100:
            duty = 100
        elif duty < -100:
            duty = -100
        # self._pwm.ChangeDutyCycle(duty)
        if self.state == 0 and duty != 0:
            GPIO.output(self._pwm_pin, GPIO.HIGH)
        else:
            GPIO.output(self._pwm_pin, GPIO.LOW)

        self.state += 1
        if self.state > 1:
            self.state = 0

    def setDir(self, dir):
        if dir == self.FREE:
            GPIO.output(self._inA_pin, GPIO.LOW)
            GPIO.output(self._inB_pin, GPIO.LOW)
        elif dir == self.BREAK:
            GPIO.output(self._inA_pin, GPIO.HIGH)
            GPIO.output(self._inB_pin, GPIO.HIGH)
        elif dir == self.FORWARD:
            GPIO.output(self._inA_pin, GPIO.LOW)
            GPIO.output(self._inB_pin, GPIO.HIGH)
        elif dir == self.BACKWARD:
            GPIO.output(self._inA_pin, GPIO.HIGH)
            GPIO.output(self._inB_pin, GPIO.LOW)

    def setSpeed(self, speed):
        if speed > 0:
            self.setDir(self.FORWARD)
            self.setDuty(speed)
        elif speed < 0:
            self.setDir(self.BACKWARD)
            self.setDuty(-speed)
        else:
            self.setDir(self.FREE)
            self.setDuty(0)


class Drive3Omni:
    """
        PinM1 -> (PWM, INA, INB) Motor #1
        PinM2 -> (PWM, INA, INB) Motor #2
        PinM3 -> (PWM, INA, INB) Motor #3
    """

    def __init__(self, pinM1, pinM2, pinM3):
        _pwmM1, _inAM1, _inBM1 = pinM1
        _pwmM2, _inAM2, _inBM2 = pinM2
        _pwmM3, _inAM3, _inBM3 = pinM3

        self.motor1 = DCMotor(_pwmM1, _inAM1, _inBM1)
        self.motor2 = DCMotor(_pwmM2, _inAM2, _inBM2)
        self.motor3 = DCMotor(_pwmM3, _inAM3, _inBM3)

        # print(self.drive((0, 0, 1)))
        # while True:
        # for duty in range(0, 101, 1):
        #     self.motor1.setDuty(duty)
        #     self.motor2.setDuty(duty)
        #     self.motor3.setDuty(duty)
        #     sleep(0.01)
        # self.motor3.setDir(self.motor3.FORWARD)
        # sleep(0.5)
        # self.motor3.setDir(self.motor3.BACKWARD)
        # for duty in range(100, -1, -1):
        #     self.motor1.setDuty(duty)
        #     self.motor2.setDuty(duty)
        #     self.motor3.setDuty(duty)
        #     sleep(0.01)
        # sleep(0.5)

    def drive(self, v, gain):
        d = 0.15
        r = 0.05
        u = [
            (v[0] * sin(pi/3) - v[1]/2 - v[2]*d)/r*gain[0],
            (v[0]*-sin(pi/3)-v[1]/2 - v[2]*d)/r*gain[1],
            (v[1] - v[2]*d)/r*gain[2]
        ]
        return u


if __name__ == "__main__":
    drive = Drive3Omni((33, 31, 29), (35, 37, 40), (32, 36, 38))

    while True:
        u = drive.drive((0, 0, 1), (1, 1, 1))
        print(u)
        drive.motor1.setSpeed(u[0])
        drive.motor2.setSpeed(u[1])
        drive.motor3.setSpeed(u[2])
        sleep(0.005)
    # for i in range(0, 5, 1):
    #     print(i)
    #     drive.motor1.setDir(drive.motor1.FORWARD)
    #     drive.motor1.setDuty(i)
    #     sleep(0.7)
    # for i in range(5, 0, -1):
    #     print(i)
    #     drive.motor1.setDuty(i)
    #     sleep(0.7)
    # drive.motor2.setSpeed(-5)
    # drive.motor3.setSpeed(-5)
    # sleep(50)
    drive.motor1.setSpeed(0)
    drive.motor2.setSpeed(0)
    drive.motor3.setSpeed(0)

    GPIO.cleanup()
