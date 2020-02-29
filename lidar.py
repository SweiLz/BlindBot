
import math
import threading
import time
import PyLidar3


from PyYDLidar.PyYDLidar import LaserScan, YDLidarX4


x = []
y = []

if __name__ == "__main__":
    # lidar = PyLidar3.YdLidarX4('/dev/ttyLidar')
    # if lidar.Connect():
    #     # print(lidar.GetDeviceInfo())
    #     gen = lidar.StartScanning()
    #     t = time.time()
    #     ll = []
    #     while time.time() < t + 100:
    #         ll = []
    #         data = next(gen)
    #         for angle in range(360):
    #             if data[angle] > 0:
    #                 ll.append((angle, data[angle]))
    #                 # print(data[angle])
    #         print(ll)
    # else:
    #     print("Error connecting to device")

    lidar = None
    while True:
        lidar = YDLidarX4("/dev/ttyUSB0")
        if lidar._isConnected:
            break
        # if lidar != None:
        #     break
        # print("Try again")
        time.sleep(1)

    # # lidar.getDeviceHealth()

    print("Tongs")
    lidar.startScanning()
    print("Liews")
    timeout = 100.0
    timeout_start = time.time()
    count = 0
    # while time.time() < timeout_start + timeout:
    while True:
        # print("y")
        lidar.getScanData()
        # print("xllllll")
        dL = []
        dR = []
        dF = []
        # print(count, len(lidar.scan.points))

        for i, point in enumerate(lidar.scan.points):
            # print("FFFFF")
            if point.dist > 0:
                p_ang = round(math.degrees(point.angle))
                if p_ang > 0 and p_ang < 10:
                    dF.append(point.dist)
                    # print(p_ang, point.dist)

            #     if p_ang > 0 and p_ang < 10:
            #         dF.append(point.dist)
            #     if p_ang > 70 and p_ang < 160:
            #         dR.append(point.dist)
            #     elif p_ang >= 160 and p_ang <= 200:
            #         dF.append(point.dist)
            #     elif p_ang > 200 and p_ang < 290:
            #         dL.append(point.dist)
        if dF != []:
            print(count, min(dF))
            count += 1
        time.sleep(0.1)
    self.lidar.stopScanning()
    # print(min(dF))
    # time.sleep(0.5)
    # print(point.angle, point.dist)

    # lidar.stopScanning()
