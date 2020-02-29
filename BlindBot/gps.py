import serial
import pynmea2

# parameter look can be =
#    GPBOD - Bearing, origin to destination
#    GPBWC - Bearing and distance to waypoint, great circle
#    GPGGA - Global Positioning System Fix Data
#    GPGLL - Geographic position, latitude / longitude
#    GPGSA - GPS DOP and active satellites
#    GPGSV - GPS Satellites in view
#    GPHDT - Heading, True
#    GPR00 - List of waypoints in currently active route
#    GPRMA - Recommended minimum specific Loran-C data
#    GPRMB - Recommended minimum navigation info
#    GPRMC - Recommended minimum specific GPS/Transit data
#    GPRTE - Routes
#    GPTRF - Transit Fix Data
#    GPSTN - Multiple Data ID
#    GPVBW - Dual Ground / Water Speed
#    GPVTG - Track made good and ground speed
#    GPWPL - Waypoint location
#    GPXTE - Cross-track error, Measured
#    GPZDA - Date & Time


class GPS:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600, timeout=2)

    def read_GPS(self):
        while True:
            strx = self.ser.readline().decode("utf-8", errors="ignore")
            if strx.find('GGA') > 0:
                data = pynmea2.parse(strx)
                return (data.latitude, data.longitude)


# if __name__ == "__main__":
#     gps = GPS("/dev/ttyS0")
#     while True:
#         data = gps.read_GPS()
#         # print(gps.ser.readline())

#         print(data)
#         # print(dir(data))
