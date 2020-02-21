# import googlemaps
import threading
import time

import serial

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

API = "AIzaSyB_x-KSdYGw4AOXM95Tx6V0JGAFFUnhOVY"


class BlindBot:
    PIN_BUZZER = 18
    PIN_TRIGGER = 7
    PIN_ECHO = 11

    def __init__(self, port):
        self._port = port
        self._baudrate = 115200
        self._isRunning = False

        self._thread_buzzer = threading.Thread(target=self._func_buzzer)
        self._thread_ultra = threading.Thread(target=self._func_ultra)
        self._thread_gps = threading.Thread(target=self._func_gps)

        self._buzzer_freq = 0.0
        self._range_ultra = 0.0

    def run(self):
        self._isRunning = True
        self._thread_buzzer.start()
        self._thread_ultra.start()
        self._thread_gps.start()

    def getCurrentLocation(self):
        pass

    def _azimuth(self, pos1, pos2):
        pass

    def _func_gps(self):
        ser = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)
        while self._isRunning:
            try:
                print(ser.readline())
            except Exception:
                print("Destroy GPS")
                self._isRunning = False
                break

    def _func_ultra(self):
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        time.sleep(1)
        while self._isRunning:
            try:
                GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
                time.sleep(0.00001)
                GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
                while GPIO.input(self.PIN_ECHO) == 0:
                    pulse_start_time = time.time()
                while GPIO.input(self.PIN_ECHO) == 1:
                    pulse_end_time = time.time()

                pulse_duration = pulse_end_time - pulse_start_time
                self._range_ultra = round(pulse_duration*17150, 2)
                time.sleep(0.05)
            except Exception:
                print("Destroy Ultrasonic")
                self._isRunning = False
                break

    def _func_buzzer(self):
        GPIO.setup(self.PIN_BUZZER, GPIO.OUT)
        buzzState = False
        while self._isRunning:
            try:
                if self._buzzer_freq > 1.0:
                    self._buzzer_freq = 1.0
                elif self._buzzer_freq < 0.0:
                    self._buzzer_freq = 0.0
                if self._buzzer_freq <= 0.03:
                    buzzState = False
                    GPIO.output(self.PIN_BUZZER, buzzState)
                    time.sleep(0.25)
                elif self._buzzer_freq >= 0.97:
                    buzzState = True
                    GPIO.output(self.PIN_BUZZER, buzzState)
                    time.sleep(0.25)
                else:
                    buzzState = not buzzState
                    GPIO.output(self.PIN_BUZZER, buzzState)
                    time.sleep(1.0-1.0*self._buzzer_freq)
            except Exception:
                print("Destroy Buzzer")
                self._isRunning = False
                break


if __name__ == "__main__":
    try:
        print("Hello World")
        robot = BlindBot("/dev/ttyUSB0")
        robot.run()
        start_time = time.time()

        while time.time() - start_time < 20:
            # strx =

            pass
            # if robot._range_ultra < 10:
            #     robot._buzzer_freq = 1.0
            # elif robot._range_ultra > 180:
            #     robot._buzzer_freq = 0.0
            # else:
            #     robot._buzzer_freq = 1.0 - (robot._range_ultra-10)/170.0
            #     print(robot._buzzer_freq)
            # pass

        # robot._buzzer_freq = 0.95
        # time.sleep(3)
        # robot._buzzer_freq = 0.1
        # time.sleep(3)

    except Exception as e:
        print(e)
        pass
    finally:
        GPIO.cleanup()


# gmaps = googlemaps.Client(key=API)

# Anman_WP = [[13.648448, 100.476775],
#             [13.648501, 100.476604],
#             [13.648865, 100.476688],
#             [13.648919, 100.476626]]


# geocode_result = gmaps.geocode("สยามพารากอน")
# print(geocode_result)
# print("\n\n")
# geocode_result = gmaps.geocode("สนามกีฬาแห่งชาติ")
# print(geocode_result)
# routes = gmaps.directions("วัดแพรก", "วัดส้มเกลี้ยง",
#                           mode="walking", language="th", units="metric", region="th")

# routes = [{
#     'bounds': {
#         'northeast': {
#             'lat': 13.8160347,
#             'lng': 100.4100009
#         },
#         'southwest': {
#             'lat': 13.813328,
#             'lng': 100.4068483}},
#     'copyrights': 'Map data ©2020',
#     'legs': [{
#         'distance': {'text': '0.6 กม.', 'value': 596},
#         'duration': {'text': '7 นาที', 'value': 441},
#         'end_address': 'บ้านเลขที่90 หมู่ที่2 ซอย วัดส้มมัณฑนา ตำบล บางคูเวียง อำเภอบางกรวย นนทบุรี 11130 ประเทศไทย',
#         'end_location': {'lat': 13.813328, 'lng': 100.4095483},
#         'start_address': 'ตำบล ปลายบาง อำเภอบางกรวย นนทบุรี 11130 ประเทศไทย',
#         'start_location': {'lat': 13.8153291, 'lng': 100.4068483},
#         'steps': [
#             {'distance': {'text': '0.1 กม.', 'value': 148},
#              'duration': {'text': '2 นาที', 'value': 106},
#              'end_location': {'lat': 13.8160347, 'lng': 100.4080042},
#              'html_instructions': 'มุ่งไปทางทิศ <b>ตะวันออกเฉียงเหนือ</b> ไปตาม <b>ถนน โครงการสายแยกวัดแพรก</b> เข้าสู่ <b>ซอย อัจฉริยะพัฒนา 10</b>',
#              'polyline': {'points': 'yhisAyuycRO]Ug@EKGK]k@y@{A'},
#              'start_location': {'lat': 13.8153291, 'lng': 100.4068483},
#              'travel_mode': 'WALKING'},

#             {'distance': {'text': '0.1 กม.', 'value': 104},
#              'duration': {'text': '1 นาที', 'value': 80},
#              'end_location': {'lat': 13.8151964, 'lng': 100.4084328},
#              'html_instructions': 'เลี้ยว <b>ขวา</b> หลังสี่แยก Nissan office (ทางด้านขวา)',
#              'maneuver': 'turn-right',
#              'polyline': {'points': 'emisA_}ycRpBw@r@]'},
#              'start_location': {'lat': 13.8160347, 'lng': 100.4080042},
#              'travel_mode': 'WALKING'},
#             {'distance': {'text': '46 ม.', 'value': 46},
#              'duration': {'text': '1 นาที', 'value': 33},
#              'end_location': {'lat': 13.8148483, 'lng': 100.4086585},
#              'html_instructions': 'ขับต่อไปยัง <b>ซอย อัจฉริยะพัฒนา</b>',
#              'polyline': {'points': '_hisAu_zcRXOJG^U'},
#              'start_location': {'lat': 13.8151964, 'lng': 100.4084328},
#              'travel_mode': 'WALKING'},
#             {'distance': {'text': '0.2 กม.', 'value': 208},
#              'duration': {'text': '3 นาที', 'value': 156},
#              'end_location': {'lat': 13.8138796, 'lng': 100.4100009},
#              'html_instructions': 'เลี้ยว<b>ซ้าย</b> เพื่อวิ่งบน <b>ซอย อัจฉริยะพัฒนา</b>',
#              'maneuver': 'turn-left',
#              'polyline': {'points': 'yeisAcazcRAIESCQCM?G?C?I@UBKJYFKFIDELGNG^QbAg@f@U'},
#              'start_location': {'lat': 13.8148483, 'lng': 100.4086585},
#              'travel_mode': 'WALKING'},
#             {'distance': {'text': '90 ม.', 'value': 90},
#              'duration': {'text': '1 นาที', 'value': 66},
#              'end_location': {'lat': 13.813328, 'lng': 100.4095483},
#              'html_instructions': 'เลี้ยว<b>ขวา</b><div style="font-size:0.9em">ปลายทางจะอยู่ทางขวา</div>',
#              'maneuver': 'turn-right',
#              'polyline': {'points': 'w_isAoizcRT\\V\\PVJN@@@?B@DADALI'},
#              'start_location': {'lat': 13.8138796, 'lng': 100.4100009},
#              'travel_mode': 'WALKING'}],
#         'traffic_speed_entry': [],
#         'via_waypoint': []}],
#     'overview_polyline': {'points': 'yhisAyuycRk@qAe@w@y@{ApBw@lAm@j@]O}@@k@Ne@NURMn@YjB}@l@z@`@h@H?RK'},
#     'summary': 'ซอย อัจฉริยะพัฒนา',
#     'warnings': ['เส้นทางเดินเท้าเป็นฟีเจอร์เบต้า ใช้ความระมัดระวัง – เส้นทางนี้อาจไม่มีทางเดินเท้าหรือบาทวิถี'],
#     'waypoint_order': []}]
# print(routes[0])
