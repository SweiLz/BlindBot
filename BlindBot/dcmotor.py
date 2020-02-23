import pigpio
import time


class DCMotor:
    FREE = 0x00
    BREAK = 0x01
    FORWARD = 0x02
    BACKWARD = 0x03
    """
    This class encapsulates a DC Motor control with pwm, inA, inB pins.
    """

    def __init__(self, pi, pwm, inA, inB):
        self.pi = pi

        self._pwm_pin = pwm
        self._inA_pin = inA
        self._inB_pin = inB

        self._pwm_pin_mode = self.pi.get_mode(self._pwm_pin)
        self._inA_pin_mode = self.pi.get_mode(self._inA_pin)
        self._inB_pin_mode = self.pi.get_mode(self._inB_pin)

        self.pi.set_mode(self._pwm_pin, pigpio.OUTPUT)
        self.pi.set_mode(self._inA_pin, pigpio.OUTPUT)
        self.pi.set_mode(self._inB_pin, pigpio.OUTPUT)

        self.pi.write(self._inA_pin, 0)
        self.pi.write(self._inB_pin, 0)
        self.pi.hardware_PWM(self._pwm_pin, 20000, 0)

        self._inited = True

    def setDuty(self, duty):
        if duty > 1.0:
            duty = 1.0
        elif duty < -1.0:
            duty = -1.0
        self.pi.hardware_PWM(self._pwm_pin, 20000, int(1e6*duty))

    def setDir(self, dir):
        if dir == self.FREE:
            self.pi.write(self._inA_pin, 0)
            self.pi.write(self._inB_pin, 0)
        elif dir == self.BREAK:
            self.pi.write(self._inA_pin, 1)
            self.pi.write(self._inB_pin, 1)
        elif dir == self.FORWARD:
            self.pi.write(self._inA_pin, 0)
            self.pi.write(self._inB_pin, 1)
        elif dir == self.BACKWARD:
            self.pi.write(self._inA_pin, 1)
            self.pi.write(self._inB_pin, 0)

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

    def cancel(self):
        """
        Cancels the motor and returns the gpios to their original mode
        """
        if self._inited:
            self._inited = False
            self.setSpeed(0)
            self.pi.set_mode(self._pwm_pin, self._pwm_pin_mode)
            self.pi.set_mode(self._inA_pin, self._inA_pin_mode)
            self.pi.set_mode(self._inB_pin, self._inB_pin_mode)


if __name__ == "__main__":
    pi = pigpio.pi()

    motor = DCMotor(pi, 13, 6, 5)
    for i in range(0, 51, 1):
        print(i)
        motor.setSpeed(i/100)
        time.sleep(0.1)
    motor.setSpeed(0)
    # end_time = time.time() + 60
    # while time.time() < end_time:
    #     time.sleep(0.03)

    motor.cancel()
    pi.stop()
