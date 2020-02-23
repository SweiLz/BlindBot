from math import atan2, cos, degrees, sin, sqrt
from time import sleep, time

from .ak8963 import AK8963
from .mpu6500 import MPU6500


class MPU9250:
    A = 0.9

    def __init__(self):
        self.mpu6500 = MPU6500(gyro_offset=(0.027998337040430993,
                                            0.00430139142048333, -0.013588545673178428))
        self.ak8963 = AK8963(offset=(0.0, -0.0896484374998181, -22.13613281249991),
                             scale=(0.9925907249361102, 0.978414201993879, 1.0304249522105178))

        self.last_data = None
        self._roll = None
        self._pitch = None

    @property
    def acceleration(self):
        """
        Acceleration measured by the sensor. By default will return a
        3-tuple of X, Y, Z axis values in m/s^2 as floats. To get values in g
        pass `accel_fs=SF_G` parameter to the MPU6500 constructor.
        """
        return self.mpu6500.acceleration

    @property
    def gyro(self):
        """
        Gyro measured by the sensor. By default will return a 3-tuple of
        X, Y, Z axis values in rad/s as floats. To get values in deg/s pass
        `gyro_sf=SF_DEG_S` parameter to the MPU6500 constructor.
        """
        return self.mpu6500.gyro

    @property
    def magnetic(self):
        """
        X, Y, Z axis micro-Tesla (uT) as floats.
        """
        return self.ak8963.magnetic

    @property
    def whoami(self):
        return self.mpu6500.whoami

    @property
    def euler(self):
        if self.last_data == None:
            self.last_data = time()
        current_data = time()
        accel = self.acceleration
        gyro = self.gyro
        mag = self.magnetic
        pitch = atan2(accel[1], sqrt((accel[0]*accel[0])+(accel[2]*accel[2])))
        roll = atan2(-accel[0],
                     sqrt((accel[1]*accel[1]) + (accel[2]*accel[2])))

        dt = current_data - self.last_data
        self.last_data = current_data

        if self._roll == None:
            self._roll = roll
        if self._pitch == None:
            self._pitch = pitch

        self._roll = self.A*(self._roll+gyro[0]*dt) + (1-self.A)*roll
        self._pitch = self.A*(self._pitch+gyro[1]*dt) + (1-self.A)*pitch
        roll = self._roll
        pitch = self._pitch
        Yh = (mag[1] * cos(roll)) - (mag[2]*sin(roll))
        Xh = (mag[0] * cos(pitch)) + (mag[1] * sin(roll) *
                                      sin(pitch)) + (mag[2] * cos(roll)*sin(pitch))

        yaw = atan2(Yh, Xh)
        return (round(degrees(roll), 2), round(degrees(pitch), 2), round(degrees(yaw), 2))


if __name__ == "__main__":
    mpu9250 = MPU9250()
    while True:
        print(mpu9250.euler)
        sleep(0.05)
    # print(mpu9250.acceleration)
    # print(mpu9250.gyro)
    # print(mpu9250.magnetic)
