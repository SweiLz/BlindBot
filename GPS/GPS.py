import serial

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


# if __name__ == "__main__":
#     ser = serial.Serial("/dev/ttyUSB0", 9600)
#     while True:
#         # if ser.readable():
#         # inCommingBytes = ser.inWaiting()
#         gpsBuffer = ser.readline()
#         print(gpsBuffer)
#         # print("")

import serial
import pynmea2


def parseGPS(strx):
    if strx.find('GGA') > 0:
        msg = pynmea2.parse(strx)
        print("Timestamp: % s - - Lat: % s % s - - Lon: % s % s - - Altitude: %s % s" %
              (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))
        print(msg.lat)


serialPort = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)
while True:
    strx = serialPort.readline().decode("utf-8", errors="ignore")
    # print(strx)
    parseGPS(strx)
# string = "$GPGGA,172333.00,1338.90484,N,10028.59334,E,1,08,0.90,19.5,M,-27.9,M,,*4D\r\n"
# print(string.find('GGA'))
