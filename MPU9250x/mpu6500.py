import struct
from time import sleep

from pycomms import PyComms


class MPU6500:
    MPU6500_ADDR = 0x68
    _GYRO_CONFIG = 0x1b
    _ACCEL_CONFIG = 0x1c
    _ACCEL_CONFIG2 = 0x1d
    _INT_PIN_CFG = 0x37
    _ACCEL_XOUT_H = 0x3b
    _ACCEL_XOUT_L = 0x3c
    _ACCEL_YOUT_H = 0x3d
    _ACCEL_YOUT_L = 0x3e
    _ACCEL_ZOUT_H = 0x3f
    _ACCEL_ZOUT_L = 0x40
    _TEMP_OUT_H = 0x41
    _TEMP_OUT_L = 0x42
    _GYRO_XOUT_H = 0x43
    _GYRO_XOUT_L = 0x44
    _GYRO_YOUT_H = 0x45
    _GYRO_YOUT_L = 0x46
    _GYRO_ZOUT_H = 0x47
    _GYRO_ZOUT_L = 0x48
    _WHO_AM_I = 0x75

    # _ACCEL_FS_MASK = 0b00011000)
    ACCEL_FS_SEL_2G = 0b00000000
    ACCEL_FS_SEL_4G = 0b00001000
    ACCEL_FS_SEL_8G = 0b00010000
    ACCEL_FS_SEL_16G = 0b00011000

    _ACCEL_SO_2G = 16384  # 1 / 16384 ie. 0.061 mg / digit
    _ACCEL_SO_4G = 8192  # 1 / 8192 ie. 0.122 mg / digit
    _ACCEL_SO_8G = 4096  # 1 / 4096 ie. 0.244 mg / digit
    _ACCEL_SO_16G = 2048  # 1 / 2048 ie. 0.488 mg / digit

    # _GYRO_FS_MASK = 0b00011000)
    GYRO_FS_SEL_250DPS = 0b00000000
    GYRO_FS_SEL_500DPS = 0b00001000
    GYRO_FS_SEL_1000DPS = 0b00010000
    GYRO_FS_SEL_2000DPS = 0b00011000

    _GYRO_SO_250DPS = 131
    _GYRO_SO_500DPS = 62.5
    _GYRO_SO_1000DPS = 32.8
    _GYRO_SO_2000DPS = 16.4

    _TEMP_SO = 333.87
    _TEMP_OFFSET = 21

    # Used for enablind and disabling the i2c bypass access
    _I2C_BYPASS_MASK = 0b00000010
    _I2C_BYPASS_EN = 0b00000010
    _I2C_BYPASS_DIS = 0b00000000

    SF_G = 1
    SF_M_S2 = 9.80665  # 1 g = 9.80665 m/s2 ie. standard gravity
    SF_DEG_S = 1
    SF_RAD_S = 0.017453292519943  # 1 deg/s is 0.017453292519943 rad/s

    def __init__(self, address=MPU6500_ADDR, accel_fs=ACCEL_FS_SEL_2G, gyro_fs=GYRO_FS_SEL_250DPS,
                 accel_sf=SF_M_S2, gyro_sf=SF_RAD_S,
                 gyro_offset=(0, 0, 0)):
        self.i2c = PyComms(address)
        self.address = address

        if 0x71 != self.whoami:
            raise RuntimeError("MPU6500 not found in I2C bus.")

        self._accel_so = self._accel_fs(accel_fs)
        self._gyro_so = self._gyro_fs(gyro_fs)
        self._accel_sf = accel_sf
        self._gyro_sf = gyro_sf
        self._gyro_offset = gyro_offset

        char = self.i2c.readU8(self._INT_PIN_CFG)
        char &= ~self._I2C_BYPASS_MASK
        char |= self._I2C_BYPASS_EN
        self.i2c.write8(self._INT_PIN_CFG, char)

        # print(self.acceleration)

    @property
    def acceleration(self):
        """
        Acceleration measured by the sensor. By default will return a
        3-tuple of X, Y, Z axis acceleration values in m/s^2 as floats. Will
        return values in g if constructor was provided `accel_sf=SF_M_S2`
        parameter.
        """
        so = self._accel_so
        sf = self._accel_sf

        xyz = xyz = self.i2c.readBytesListU(self._ACCEL_XOUT_H, 6)
        xyz = list(struct.unpack(">hhh", bytes(xyz)))
        return tuple([value / so * sf for value in xyz])

    @property
    def gyro(self):
        """
        X, Y, Z radians per second as floats.
        """
        so = self._gyro_so
        sf = self._gyro_sf
        ox, oy, oz = self._gyro_offset

        xyz = self.i2c.readBytesListU(self._GYRO_XOUT_H, 6)
        xyz = list(struct.unpack(">hhh", bytes(xyz)))
        xyz = [value / so * sf for value in xyz]

        xyz[0] -= ox
        xyz[1] -= oy
        xyz[2] -= oz

        return tuple(xyz)

    @property
    def temperature(self):
        """
        Die temperature in celcius as a float.
        """
        temp = self.i2c.readU16(self._TEMP_OUT_H)
        return ((temp - self._TEMP_OFFSET) / self._TEMP_SO) + self._TEMP_OFFSET

    @property
    def whoami(self):
        """ Value of the whoami register. """
        return self.i2c.readU8(self._WHO_AM_I)

    def calibrate(self, count=256, delay=100):
        ox, oy, oz = (0.0, 0.0, 0.0)
        self._gyro_offset = (0.0, 0.0, 0.0)
        n = count

        while count:
            print(count)
            sleep(delay/1000)
            gx, gy, gz = self.gyro
            ox += gx
            oy += gy
            oz += gz
            count -= 1

        self._gyro_offset = (ox / n, oy / n, oz / n)
        return self._gyro_offset

    def _accel_fs(self, value):
        self.i2c.write8(self._ACCEL_CONFIG, value)

        # Return the sensitivity divider
        if self.ACCEL_FS_SEL_2G == value:
            return self._ACCEL_SO_2G
        elif self.ACCEL_FS_SEL_4G == value:
            return self._ACCEL_SO_4G
        elif self.ACCEL_FS_SEL_8G == value:
            return self._ACCEL_SO_8G
        elif self.ACCEL_FS_SEL_16G == value:
            return self._ACCEL_SO_16G

    def _gyro_fs(self, value):
        self.i2c.write8(self._GYRO_CONFIG, value)

        # Return the sensitivity divider
        if self.GYRO_FS_SEL_250DPS == value:
            return self._GYRO_SO_250DPS
        elif self.GYRO_FS_SEL_500DPS == value:
            return self._GYRO_SO_500DPS
        elif self.GYRO_FS_SEL_1000DPS == value:
            return self._GYRO_SO_1000DPS
        elif self.GYRO_FS_SEL_2000DPS == value:
            return self._GYRO_SO_2000DPS


if __name__ == "__main__":
    mpu6500 = MPU6500(gyro_offset=(0.021079159915769665,
                                   0.00029300464243582684, -0.012618455702485027))
    # print(mpu6500.calibrate())
    # while True:
    # print(mpu6500.gyro, mpu6500.acceleration)
    # sleep(0.15)
