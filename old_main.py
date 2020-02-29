import math
import threading
import time

import pigpio
from BlindBot.driver import Omni3Wheel
from BlindBot.gps import GPS
from BlindBot.sonar import Sonar
from MPU9250.mpu9250 import MPU9250


class Robot:
    def __init__(self):
        self.pi = pigpio.pi()
        self._isRunning = False

        self._thread_buzzer = threading.Thread(target=self._func_buzzer)
        self._thread_ultra = threading.Thread(target=self._func_ultra)
        self._thread_gps = threading.Thread(target=self._func_gps)
        self._thread_drive = threading.Thread(target=self._func_drive)
        self._thread_imu = threading.Thread(target=self._func_imu)

        self._buzzer_freq = 0.5
        self._range_ultra = 0.0
        self._drive_speed = [0.0, 0.0, 0.0]
        self._gps_lat_lon = [0.0, 0.0]
        self._imu_head = 0.0
        self._gps_isOk = False

    def run(self):
        self._isRunning = True
        self._thread_buzzer.start()
        self._thread_ultra.start()
        self._thread_imu.start()
        self._thread_gps.start()
        self._thread_drive.start()

    def _func_gps(self):
        gps = GPS("/dev/ttyS0")
        while self._isRunning:
            try:
                lat, lon = gps.read_GPS()
                if lat == 0 or lon == 0:
                    self._gps_isOk = False
                    continue
                self._gps_isOk = True
                self._gps_lat_lon[0] = lat
                self._gps_lat_lon[1] = lon
            except Exception:
                print("Destroy GPS")
                self._isRunning = False
                break

    def _func_ultra(self):
        sonar_trig = 27
        sonar_echo = 22
        sonar = Sonar(self.pi, sonar_trig, sonar_echo)
        while self._isRunning:
            try:
                self._range_ultra = sonar.getDist()
                time.sleep(0.1)
            except Exception:
                print("Destroy Sonar")
                self._isRunning = False
                break
        sonar.cancel()

    def _func_buzzer(self):
        buzzState = False
        buzz_pin = 23
        while self._isRunning:
            try:
                if self._buzzer_freq > 1.0:
                    self._buzzer_freq = 1.0
                elif self._buzzer_freq < 0.0:
                    self._buzzer_freq = 0.0
                if self._buzzer_freq <= 0.03:
                    buzzState = False
                    self.pi.write(buzz_pin, buzzState)
                    time.sleep(0.25)
                elif self._buzzer_freq >= 0.97:
                    buzzState = True
                    self.pi.write(buzz_pin, buzzState)
                    time.sleep(0.25)
                else:
                    buzzState = not buzzState
                    self.pi.write(buzz_pin, buzzState)
                    time.sleep(1.0-1.0*self._buzzer_freq)
            except Exception:
                print("Destroy Buzzer")

                self._isRunning = False
                break
        self.pi.write(buzz_pin, 0)

    def _func_drive(self):

        base = Omni3Wheel(self.pi, (13, 6, 5), (19, 26, 21),
                          (12, 16, 20), 0.05, 0.15, (0.1, 0.1, 0.1))
        while self._isRunning:
            try:
                base.drive(self._drive_speed)
                time.sleep(0.05)
            except Exception:
                print("Destroy Drive")
                self._isRunning = False
                break
        base.drive((0, 0, 0))

    def _func_imu(self):
        imu = MPU9250()
        imu.initAK8963()
        while self._isRunning:
            try:
                imu.update()
                self._imu_head = -imu.euler[2]+180.0
                time.sleep(0.02)
            except Exception:
                print("Destroy IMU")
                self._isRunning = False
                break

    def stop(self):
        self.pi.stop()

    @staticmethod
    def _cal_distance_bearing(pointA, pointB):
        lat1, lon1 = math.radians(pointA[0]), math.radians(pointA[1])
        lat2, lon2 = math.radians(pointB[0]), math.radians(pointB[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + \
            math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = 6373000 * c
        y = math.sin(dlon) * math.cos(lat2)
        x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1) * \
            math.cos(lat2)*math.cos(dlon)
        brng = math.degrees(math.atan2(y, x))
        compass_bearing = (brng + 360) % 360

        return (distance, compass_bearing)

    def goToWaypoint(self, goal_point):
        if not self._gps_isOk:
            self._buzzer_freq = 0.95
            time.sleep(1.5)
            self._buzzer_freq = 0
            print("GPS not detect")
            return False
        dist = self._cal_distance_bearing(
            self._gps_lat_lon, goal_point)[0]

        sum_turn = 0
        while dist > 3:
            dist, heading = self._cal_distance_bearing(
                self._gps_lat_lon, goal_point)
            compass_diff = math.radians(heading - self._imu_head)
            turn = math.atan2(math.sin(compass_diff), math.cos(compass_diff))
            v = 0.1
            w = turn * 0.9  # + sum_turn*0.01
            sum_turn += turn
            # print(v, w)
            # print(heading, math.degrees(compass_diff), sum_turn)
            print(dist)
            robot._drive_speed = (0, 0.0, w)
            time.sleep(0.05)
        robot._drive_speed = (0, 0, 0)
        return True


if __name__ == "__main__":
    try:
        robot = Robot()

        robot.run()

        # list_waypoint = [
        #     (13.6485062, 100.4765653),
        #     (13.6489503, 100.476647),
        #     (13.6490773, 100.4759503),
        #     (13.6512976, 100.4762667),
        #     (13.6512955, 100.4763166),
        #     (13.6513551, 100.4763059),
        # ]
        # for point in list_waypoint:
        #     if not robot.goToWaypoint(point):
        #         break

        end_time = time.time() + 600
        while time.time() < end_time:

            # robot._buzzer_freq = 0.5
            # print(robot._imu_head)
            # print(robot._gps_lat_lon)
            # print(robot._range_ultra)
            # w = -robot._imu_head * 0.1
            # print(w)
            # robot._drive_speed = (0.12, 0.0, 0)
            # print(robot._gps_lat_lon)
            time.sleep(0.2)

        robot.stop()

    except KeyboardInterrupt:
        pass
    finally:
        robot._buzzer_freq = 0
        robot._drive_speed = (0, 0, 0)
