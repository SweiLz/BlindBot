import threading
from time import sleep, time
from math import radians, degrees, atan2, sin, cos, sqrt
import serial
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import pigpio
from BlindBot.driver import Omni3Wheel
from BlindBot.gps import GPS
from BlindBot.sonar import Sonar
from MPU9250.mpu9250 import MPU9250
from PyYDLidar.PyYDLidar import LaserScan, YDLidarX4


app = Flask(__name__)
api = Api(app)

# sleep(10)
# @app.before_first_request
# def initialize():
#     pass


class Robot:
    def __init__(self):
        self.pi = pigpio.pi()
        self._isRunning = False

        self._thread_buzzer = threading.Thread(target=self._func_buzzer)
        self._buzzer_freq = 0.0

        self._thread_drive = threading.Thread(target=self._func_drive)
        self._drive_speed = [0.0, 0.0, 0.0]

        self._thread_gps_ultra = threading.Thread(target=self._func_gps_ultra)
        self._gps_isOk = False
        self._gps_location = None
        self._range_ultra = 0.0

        self._thread_imu = threading.Thread(target=self._func_imu)
        self._imu_head = 0.0

        self._thread_control = threading.Thread(target=self._func_control)
        self._control_flag = False
        self._target_head = 0.0
        self._target_speed = 0.0
        self._target_dist = 0.0

        self._thread_lidar = threading.Thread(target=self._func_lidar)
        self._lidar_detect = [0, 0, 0]

        self._ultra_buzzer_enable = True
        self._ultra_threshold_stop = 150  # cm
        self._ultra_sound_freq = 0.85  # % 0.0 -> 1.0

        self._lidar_enable = False
        self._threshold_side = 0.5
        self._threshold_front = 0.7

        self._speed = 0.2

    def run(self):
        self._isRunning = True
        self._thread_buzzer.start()
        self._buzzer_freq = 0.95
        sleep(0.5)
        self._buzzer_freq = 0
        self._thread_drive.start()

        self._thread_gps_ultra.start()
        self._thread_imu.start()
        self._thread_control.start()
        self._thread_lidar.start()

    def stop(self):
        self._isRunning = False
        self._control_flag = False

    def _func_buzzer(self):
        buzzState = False
        buzz_pin = 23
        while self._isRunning:
            self._buzzer_freq = max(0, min(1.0, self._buzzer_freq))
            if self._buzzer_freq <= 0.03:
                buzzState = False
                self.pi.write(buzz_pin, buzzState)
                sleep(0.25)
            elif self._buzzer_freq >= 0.97:
                buzzState = True
                self.pi.write(buzz_pin, buzzState)
                sleep(0.25)
            else:
                buzzState = not buzzState
                self.pi.write(buzz_pin, buzzState)
                sleep(1.0-1.0*self._buzzer_freq)
        self.pi.write(buzz_pin, 0)

    def _func_drive(self):
        base = Omni3Wheel(self.pi, (13, 6, 5), (19, 26, 21),
                          (12, 16, 20), 0.05, 0.15, (0.1, 0.1, 0.1))
        while self._isRunning:
            base.drive(self._drive_speed)
            sleep(0.1)
        base.drive((0, 0, 0))

    def _func_gps_ultra(self):
        gps = GPS("/dev/ttyS0")
        sonar_trig = 27
        sonar_echo = 22
        sonar = Sonar(self.pi, sonar_trig, sonar_echo)
        while self._isRunning:
            self._range_ultra = sonar.getDist()
            lat, lon = gps.read_GPS()
            if lat == 0 or lon == 0:
                self._gps_isOk = False
                continue
            self._gps_isOk = True
            if self._gps_location == None:
                self._gps_location = [lat, lon]
            else:
                self._gps_location[0] = lat * 0.5 + self._gps_location[0]*0.5
                self._gps_location[1] = lon * 0.5 + self._gps_location[1]*0.5

            # print(self._gps_location)
        sonar.cancel()

    def _func_imu(self):
        imu = MPU9250()
        imu.initMPU9250()
        imu.initAK8963()
        last_data = time()
        _roll = None
        _pitch = None
        _yaw = None
        while self._isRunning:
            accel = imu.data_accel
            gyro = imu.data_gyro
            mag = imu.data_mag
            pitch = atan2(accel[1], sqrt(
                (accel[0]*accel[0])+(accel[2]*accel[2])))
            roll = atan2(-accel[0],
                         sqrt((accel[1]*accel[1]) + (accel[2]*accel[2])))

            current_data = time()
            dt = current_data - last_data
            last_data = current_data
            if _roll == None:
                _roll = roll
            if _pitch == None:
                _pitch = pitch

            _roll = 0.85*(_roll+gyro[0]*dt) + 0.1*_roll + 0.05*roll
            _pitch = 0.85*(_pitch+gyro[1]*dt) + 0.1*_pitch + 0.05*roll
            Yh = (mag[1] * cos(_roll)) - (mag[2]*sin(_roll))
            Xh = (mag[0] * cos(_pitch)) + (mag[1] * sin(_roll) *
                                           sin(_pitch)) + (mag[2] * cos(roll)*sin(_pitch))

            _yaw = atan2(Yh, Xh)
            self._imu_head = degrees(_yaw)
            # print(self._imu_head)
            sleep(0.05)

    def _func_lidar(self):
        self._lidar_detect = [0, 0, 0]
        lidar = YDLidarX4("/dev/ttyLidar")
        lidar.startScanning()
        sleep(3)
        gen = lidar.getScanData()
        while self._isRunning:
            dF = [[], [], []]
            for point in next(gen):
                if point.dist > 0.05:
                    p_ang = round(degrees(point.angle)) + 180
                    if p_ang > 35 and p_ang < 95:
                        dF[0].append(point.dist)
                    elif p_ang > 350 or p_ang < 10:
                        dF[1].append(point.dist)
                    elif p_ang > 235 and p_ang < 325:
                        dF[2].append(point.dist)

            if dF[0] != []:
                if min(dF[0]) < self._threshold_side:
                    self._lidar_detect[0] = 1  # min(dF[0])
                else:
                    self._lidar_detect[0] = 0
            if dF[1] != []:
                if min(dF[1]) < self._threshold_front:
                    self._lidar_detect[1] = 1  # min(dF[1])
                else:
                    self._lidar_detect[1] = 0
            if dF[2] != []:
                if min(dF[2]) < self._threshold_side:
                    self._lidar_detect[2] = 1  # min(dF[2])
                else:
                    self._lidar_detect[2] = 0

        lidar.stopScanning()

    def _func_control(self):
        self._control_flag = False
        while self._isRunning:
            if self._control_flag:

                compass_diff = radians(
                    self._target_head+94 - self._imu_head)
                turn = atan2(sin(compass_diff), cos(compass_diff))
                self._speed = self._target_speed
                vx = self._speed
                w = max(min(-turn * 1.5, 0.6), -0.6)
                # print(turn, w)
                if abs(degrees(turn)) < 15:
                    vx = self._speed

                vy = 0.0

                if self._lidar_enable:
                    if self._lidar_detect[0] and self._lidar_detect[2]:
                        vy = 0.0
                    elif self._lidar_detect[0]:
                        vy = -0.1
                    elif self._lidar_detect[2]:
                        vy = 0.1
                    if self._lidar_detect[1]:
                        vx = 0.0
                if self._ultra_buzzer_enable:
                    # print(self._range_ultra)
                    if self._range_ultra > 10 and self._range_ultra < self._ultra_threshold_stop:
                        self._buzzer_freq = self._ultra_sound_freq
                        vx = 0.0
                        vy = 0.0
                        w = 0.0
                    else:
                        self._buzzer_freq = 0.0

                self._drive_speed = (vx, vy, w)
                # print(self._drive_speed)
                # print((vx, vy, w))
            sleep(0.05)
        self._drive_speed = [0, 0, 0]


robot = Robot()

# Robot Speed
robot._speed = 0.2  # % 0.0 -> 1.0
# Ultrasonic and Buzzer
robot._ultra_buzzer_enable = True
robot._ultra_threshold_stop = 60  # cm
robot._ultra_sound_freq = 0.85  # % 0.0 -> 1.0
# Lidar Enable
robot._lidar_enable = True
robot._threshold_side = 0.5  # m
robot._threshold_front = 0.7  # m
#######
robot.run()


class RobotAPI(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Heading', type=float)
        self.parser.add_argument('Speed', type=float)
        self.parser.add_argument('BuzzerFrq', type=float)
        self.parser.add_argument('DriveSpeed',  action='split', type=float)
        self.parser.add_argument('DriveX', type=float)
        self.parser.add_argument('DriveY', type=float)

        super().__init__()

    def get(self, id=None):
        if id == 201:
            ret = {
                'GPS': robot._gps_location if robot._gps_isOk else [0, 0]
            }
            return ret, 201
        elif id == 220:
            robot._control_flag = False
            robot._drive_speed = [0, 0, 0]
            return "OK", 220
            # 'Sonar': robot._range_ultra,
            # 'IMU': degrees(robot.gggg)
        return "FAIL", 601

    def post(self, id):
        if id == 221:
            args = self.parser.parse_args()
            robot._target_head = args['Heading']
            robot._target_speed = args['Speed']
            robot._control_flag = True
            return "OK", 221
        return None

    def put(self, id):
        ret = {}
        code = 200
        if id == "head":
            args = self.parser.parse_args()
            if args.get('Head') != None:
                robot._target_head = args['Head']
                robot._control_flag = True
        elif id == "data":
            parser.add_argument('TargetHead', type=float)
            parser.add_argument('TargetDist', type=float)
            args = parser.parse_args()
            if args.get('TargetHead') != None:
                robot._target_head = args['TargetHead']
            if args.get('TargetDist') != None:
                robot._target_dist = args['TargetDist']

            code = 609
        elif id == "command":
            args = self.parser.parse_args()
            if args.get('BuzzerFrq') != None:
                robot._buzzer_freq = args['BuzzerFrq']
            if args.get('DriveSpeed') != None:
                robot._drive_speed = args['DriveSpeed']
            else:
                if args.get('DriveX') != None:
                    robot._drive_speed[0] = args['DriveX']
                if args.get('DriveY') != None:
                    robot._drive_speed[1] = args['DriveY']
            robot._control_flag = False
            code = 610
        return ret, code


api.add_resource(RobotAPI, '/', '/<int:id>')
if __name__ == "__main__":
    app.run(host="192.168.4.1", debug=False)
    robot.stop()
