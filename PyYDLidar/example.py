from PyYDLidar import YDLidarX4
from time import sleep, time
from math import degrees

print("Hello World")

lidar = YDLidarX4("/dev/ttyLidar")
lidar.startScanning()
sleep(3)
count = 0
pp = [10]*361

gen = lidar.getScanData()
t = time()
while (time() - t) < 120:
    dF = [[], [], []]

    for i, point in enumerate(next(gen)):
        if point.dist > 0.05:
            p_ang = round(degrees(point.angle))+180
            if p_ang > 35 and p_ang < 95:
                dF[0].append(point.dist)
            elif p_ang > 350 or p_ang < 10:
                dF[1].append(point.dist)
            elif p_ang > 235 and p_ang < 325:
                dF[2].append(point.dist)
    print(min(dF[0]), min(dF[1]), min(dF[2]))
    # print("\n")
#     if point.dist > 0.05:
#         p_ang = round(degrees(point.angle)) + 180
    # print(count, next(gen)[0])
    # count += 1
    # lidar.getScanData()
    # pass

#     lidar.getScanData()
#     print(len(lidar.scan.points))
# for i, point in enumerate(lidar.scan.points):

#     if point.dist > 0.05:
#         p_ang = round(degrees(point.angle)) + 180
#         # print(p_ang, point.dist)
#         if p_ang > 35 and p_ang < 95:
#             dF[0].append(point.dist)
#         elif p_ang > 350 or p_ang < 10:
#             pp[p_ang] = (p_ang, point.dist)
#             # print(point.dist)
#             # dF[1].append(point.dist)

#         elif p_ang > 235 and p_ang < 325:
#             dF[2].append(point.dist)
# print(dF[1])
# if dF[0] != []:
#     self._xl = min(dF[0])
#     # if min(dF[0]) < self._threshold_side:
#     #     self._lidar_detect[0] = 1
#     # else:
#     #     self._lidar_detect[0] = 0
# if dF[1] != []:
#     self._xf = min(dF[1])
#     # if min(dF[1]) < self._threshold_front:
#     #     self._lidar_detect[1] = 1
#     # else:
#     #     self._lidar_detect[1] = 0
# if dF[2] != []:
#     self._xr = min(dF[2])
# if min(dF[2]) < self._threshold_side:
#     self._lidar_detect[2] = 1
# else:
#     self._lidar_detect[2] = 0
# print(count, self._xl, self._xf, self._xr)
# print(count, pp[350:])
# count += 1
# sleep(0.1)
# lidar.stopScanning()
