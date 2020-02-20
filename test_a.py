import math

import matplotlib.pyplot as plt
import numpy as np

from PyYDLidar.PyYDLidar import LaserScan, YDLidarX4

show_animation = True


def dwa_control(x, config, goal, ob):
    """
    Dynamic Window Approach control
    """

    dw = calc_dynamic_window(x, config)

    u, trajectory = calc_control_and_trajectory(x, dw, config, goal, ob)

    return u, trajectory


class Config:
    """
    simulation parameter class
    """

    def __init__(self):
        # robot parameter
        self.max_speed = 0.5  # [m/s]
        self.min_speed = -0.2  # [m/s]
        self.max_yawrate = 180.0 * math.pi / 180.0  # [rad/s]
        self.max_accel = 0.2  # [m/ss]
        self.max_dyawrate = 40.0 * math.pi / 180.0  # [rad/ss]
        self.v_reso = 0.01  # [m/s]
        self.yawrate_reso = 0.1 * math.pi / 180.0  # [rad/s]
        self.dt = 0.1  # [s] Time tick for motion prediction
        self.predict_time = 5.0  # [s]
        self.to_goal_cost_gain = 1.5
        self.speed_cost_gain = 0.5
        self.obstacle_cost_gain = 0.15

        # if robot_type == RobotType.circle
        # Also used to check if goal is reached in both types
        self.robot_radius = 0.25  # [m] for collision check


def motion(x, u, dt):
    """
    motion model
    """

    x[2] += u[1] * dt  # Yaw (rad)
    x[0] += u[0] * math.cos(x[2]) * dt  # Position X (m)
    x[1] += u[0] * math.sin(x[2]) * dt  # Position Y (m)
    x[3] = u[0]  # vx (m/s)
    x[4] = u[1]  # wz (rad/s)

    return x


def calc_dynamic_window(x, config):
    """
    calculation dynamic window based on current state x
    """

    # Dynamic window from robot specification
    Vs = [config.min_speed, config.max_speed,
          -config.max_yawrate, config.max_yawrate]

    # Dynamic window from motion model
    Vd = [x[3] - config.max_accel * config.dt,
          x[3] + config.max_accel * config.dt,
          x[4] - config.max_dyawrate * config.dt,
          x[4] + config.max_dyawrate * config.dt]

    #  [vmin, vmax, yaw_rate min, yaw_rate max]
    dw = [max(Vs[0], Vd[0]), min(Vs[1], Vd[1]),
          max(Vs[2], Vd[2]), min(Vs[3], Vd[3])]

    return dw


def predict_trajectory(x_init, v, y, config):
    """
    predict trajectory with an input
    """

    x = np.array(x_init)
    traj = np.array(x)
    time = 0
    while time <= config.predict_time:
        x = motion(x, [v, y], config.dt)
        traj = np.vstack((traj, x))
        time += config.dt

    return traj


def calc_control_and_trajectory(x, dw, config, goal, ob):
    """
    calculation final input with dynamic window
    """

    x_init = x[:]
    min_cost = float("inf")
    best_u = [0.0, 0.0]
    best_trajectory = np.array([x])

    # evaluate all trajectory with sampled input in dynamic window
    for v in np.arange(dw[0], dw[1], config.v_reso):
        for y in np.arange(dw[2], dw[3], config.yawrate_reso):

            trajectory = predict_trajectory(x_init, v, y, config)

            # calc cost

            to_goal_cost = config.to_goal_cost_gain * \
                calc_to_goal_cost(trajectory, goal)

            speed_cost = config.speed_cost_gain * \
                (config.max_speed - trajectory[-1, 3])
            if ob.size == 0:
                ob_cost = 0
            else:
                ob_cost = config.obstacle_cost_gain * \
                    calc_obstacle_cost(trajectory, ob, config)

            final_cost = to_goal_cost + speed_cost + ob_cost

            # search minimum trajectory
            if min_cost >= final_cost:
                min_cost = final_cost
                best_u = [v, y]
                best_trajectory = trajectory

    return best_u, best_trajectory


def calc_obstacle_cost(trajectory, ob, config):
    """
        calc obstacle cost inf: collision
    """
    ox = ob[:, 0]
    oy = ob[:, 1]
    dx = trajectory[:, 0] - ox[:, None]
    dy = trajectory[:, 1] - oy[:, None]
    r = np.hypot(dx, dy)

    if (r <= config.robot_radius).any():
        return float("Inf")

    min_r = np.min(r)
    return 1.0 / min_r  # OK


def calc_to_goal_cost(trajectory, goal):
    """
        calc to goal cost with angle difference
    """

    dx = goal[0] - trajectory[-1, 0]
    dy = goal[1] - trajectory[-1, 1]
    error_angle = math.atan2(dy, dx)
    cost_angle = error_angle - trajectory[-1, 2]
    cost = abs(math.atan2(math.sin(cost_angle), math.cos(cost_angle)))

    return cost


def plot_arrow(x, y, yaw, length=0.5, width=0.1):  # pragma: no cover
    plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw),
              head_length=width, head_width=width)
    plt.plot(x, y)


def plot_robot(x, y, yaw, config):  # pragma: no cover

    circle = plt.Circle((x, y), config.robot_radius, color="b")
    plt.gcf().gca().add_artist(circle)
    # out_x, out_y = (np.array([x, y]) +
    #                 np.array([np.cos(yaw), np.sin(yaw)]) * config.robot_radius)
    # plt.plot([x, out_x], [y, out_y], "-k")


def getOb(x, scan):
    if len(scan) != 0:
        ob = np.zeros((len(scan), 2))
        for i in range(len(scan)):
            dist = scan[i].dist
            angle = scan[i].angle + x[2] + np.pi

            ob[i] = [x[0] + dist * np.cos(angle), x[1]+dist * np.sin(angle)]
        return ob
    else:
        return np.array([])


if __name__ == '__main__':

    print("Hello World")
    try:
        lidar = YDLidarX4("/dev/ttyUSB0")
        lidar.startScanning()

        gx, gy = 2.5, 0
        # initial state [x(m), y(m), yaw(rad), v(m/s), omega(rad/s)]
        x = np.array([0.0, 0.0, 0, 0.0, 0.0])
        # goal position [x(m), y(m)]
        goal = np.array([gx, gy])
        # obstacles [x(m) y(m), ....]

        # ob = np.array([[-0.5, -0.5]])
        # ob = np.array([])

        # input [forward speed, yaw_rate]
        config = Config()

        trajectory = np.array(x)

        while True:
            lidar.getScanData()
            ob = getOb(x, lidar.scan.points)
            # print(x)

            u, predicted_trajectory = dwa_control(x, config, goal, ob)
            u = [0, 0]
            x = motion(x, u, config.dt)  # simulate robot
            # dist = math.sqrt((goal[0] - x[0])**2+(goal[1] - x[1])**2)
            # if dist < 2.5:
            #     goal[0] = 0.0
            #     goal[1] = 15.0
            #     dd = np.array([[5, 0], [5, 1], [5, 2], [5, 3], [5, 10], [5, 12]])
            #     ob = np.append(ob, dd, axis=0)

            trajectory = np.vstack((trajectory, x))  # store state history

            if show_animation:
                plt.cla()
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event',
                                             lambda event: [exit(0) if event.key == 'escape' else None])
                plt.plot(predicted_trajectory[:, 0],
                         predicted_trajectory[:, 1], "-g")
                plt.plot(x[0], x[1], "xr")
                plt.plot(goal[0], goal[1], "xb")
                if ob.size != 0:
                    plt.scatter(ob[:, 0],  ob[:, 1], c='r', s=1)
                    # plt.plot(ob[:, 0], ob[:, 1], "ok")
                plot_robot(x[0], x[1], x[2], config)
                plot_arrow(x[0], x[1], x[2])
                plt.axis("equal")
                plt.grid(True)
                plt.pause(0.0001)

            # check reaching goal
            dist_to_goal = math.hypot(x[0] - goal[0], x[1] - goal[1])
            if dist_to_goal <= config.robot_radius:
                print("Goal!!")
                break

        print("Done")
        if show_animation:
            plt.plot(trajectory[:, 0], trajectory[:, 1], "-r")
            plt.pause(0.0001)
        plt.show()
        lidar.stopScanning()
    except KeyboardInterrupt:
        exit()
