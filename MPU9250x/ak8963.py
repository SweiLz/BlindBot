import struct
from time import sleep

from pycomms import PyComms


class AK8963:
    AK8963_ADDR = 0x0C
    AK8963_ST1 = 0x02
    _WIA = 0x00
    _HXL = 0x03
    _HXH = 0x04
    _HYL = 0x05
    _HYH = 0x06
    _HZL = 0x07
    _HZH = 0x08
    _ST2 = 0x09
    _CNTL1 = 0x0a
    _ASAX = 0x10
    _ASAY = 0x11
    _ASAZ = 0x12

    _MODE_POWER_DOWN = 0b00000000
    MODE_SINGLE_MEASURE = 0b00000001
    MODE_CONTINOUS_MEASURE_1 = 0b00000010  # 8Hz
    MODE_CONTINOUS_MEASURE_2 = 0b00000110  # 100Hz
    MODE_EXTERNAL_TRIGGER_MEASURE = 0b00000100
    _MODE_SELF_TEST = 0b00001000
    _MODE_FUSE_ROM_ACCESS = 0b00001111

    OUTPUT_14_BIT = 0b00000000
    OUTPUT_16_BIT = 0b00010000

    _SO_14BIT = 0.6  # μT per digit when 14bit mode
    _SO_16BIT = 0.15  # μT per digit when 16bit mode

    def __init__(self, address=AK8963_ADDR, offset=(0, 0, 0), scale=(1, 1, 1)):
        self.i2c = PyComms(address)
        self.address = address
        self._offset = offset
        self._scale = scale

        if 0x48 != self.whoami:
            raise RuntimeError("AK8963 not found in I2C bus.")

        self.i2c.write8(self._CNTL1, self._MODE_FUSE_ROM_ACCESS)
        asax = self.i2c.readU8(self._ASAX)
        asay = self.i2c.readU8(self._ASAY)
        asaz = self.i2c.readU8(self._ASAZ)
        self.i2c.write8(self._CNTL1, self._MODE_POWER_DOWN)

        self._adjustment = (
            (0.5 * (asax - 128)) / 128 + 1,
            (0.5 * (asay - 128)) / 128 + 1,
            (0.5 * (asaz - 128)) / 128 + 1
        )

        self.i2c.write8(
            self._CNTL1, (self.MODE_CONTINOUS_MEASURE_1 | self.OUTPUT_16_BIT))
        self._so = self._SO_16BIT

        # print(self._adjustment)
        # print(self.magnetic)

    @property
    def magnetic(self):
        """
        X, Y, Z axis micro-Tesla (uT) as floats.
        """

        # xyz = [self.i2c.readS16(self._HXL), self.i2c.readS16(
        #     self._HYL), self.i2c.readS16(self._HZL)]
        # self.i2c.readU8(self._ST2)
        xyz = self.i2c.readBytesListU(self._HXL, 6)
        xyz = list(struct.unpack("<hhh", bytes(xyz)))
        self.i2c.readU8(self._ST2)

        # print("xyz:", xyz)
        # print("xyz2:", xyz2)

        # Apply factory axial sensitivy adjustements
        xyz[0] *= self._adjustment[0]
        xyz[1] *= self._adjustment[1]
        xyz[2] *= self._adjustment[2]

        # Apply output scale determined in constructor
        so = self._so
        xyz[0] *= so
        xyz[1] *= so
        xyz[2] *= so

        # Apply hard iron ie. offset bias from calibration
        xyz[0] -= self._offset[0]
        xyz[1] -= self._offset[1]
        xyz[2] -= self._offset[2]

        # Apply soft iron ie. scale bias from calibration
        xyz[0] *= self._scale[0]
        xyz[1] *= self._scale[1]
        xyz[2] *= self._scale[2]

        return tuple(xyz)

    @property
    def adjustement(self):
        return self._adjustment

    @property
    def whoami(self):
        """ Value of the whoami register. """
        return self.i2c.readU8(self._WIA)

    def calibrate(self, count=256, delay=200):
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)

        reading = self.magnetic
        minx = maxx = reading[0]
        miny = maxy = reading[1]
        minz = maxz = reading[2]

        while count:
            print(count)
            sleep(delay/1000)
            reading = self.magnetic
            minx = min(minx, reading[0])
            maxx = max(maxx, reading[0])
            miny = min(miny, reading[1])
            maxy = max(maxy, reading[1])
            minz = min(minz, reading[2])
            maxz = max(maxz, reading[2])
            count -= 1

        offset_x = (maxx + minx) / 2
        offset_y = (maxy + miny) / 2
        offset_z = (maxz + minz) / 2

        self._offset = (offset_x, offset_y, offset_z)

        avg_delta_x = (maxx - minx) / 2
        avg_delta_y = (maxy - miny) / 2
        avg_delta_z = (maxz - minz) / 2

        avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

        scale_x = avg_delta / avg_delta_x
        scale_y = avg_delta / avg_delta_y
        scale_z = avg_delta / avg_delta_z

        self._scale = (scale_x, scale_y, scale_z)

        return self._offset, self._scale


if __name__ == "__main__":
    # ak8963 = AK8963(offset=(235.83749999999998, -21.515625, -186.219140625),
    #                 scale=(0.7273713128976287, 0.752956144289777, 3.3660086985613935))
    ak8963 = AK8963()
    print(ak8963.calibrate())
    while True:
        print(ak8963.magnetic)
        sleep(0.1)
