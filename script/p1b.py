#!/usr/bin/env python3
import math
import random
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import Kill, Spawn

hunter_pos = [0, 0]
runner_pos = [0, 0]

def too_close():
    x = hunter_pos
    y = runner_pos
    if ((x[1] - y[1]) ** 2 + (x[0] - y[0]) ** 2) ** 0.5 < 1:
        return True
    return False

def hunter_subscriber_callback(message):
    hunter_pos[0] = message.x
    hunter_pos[1] = message.y

def runner_subscriber_callback(message):
    runner_pos[0] = message.x
    runner_pos[1] = message.y

def p1a():
    hunter_subscriber = rospy.Subscriber('/hunter/pose', Pose, hunter_subscriber_callback)
    runner_subscriber = rospy.Subscriber('/runner/pose', Pose, runner_subscriber_callback)

    hunter_publisher = rospy.Publisher('/hunter/cmd_vel', Twist, queue_size=10)
    runner_publisher = rospy.Publisher('/runner/cmd_vel', Twist, queue_size=10)

    kill_proxy = rospy.ServiceProxy('/kill', Kill)
    spawn_proxy = rospy.ServiceProxy('/spawn', Spawn)

    rospy.init_node('turtle_controller', anonymous=True)
    hz = 10
    rate = rospy.Rate(hz)
    kill_proxy("turtle1")

    time_since_last_runner_direction_change = 0
    runner_direction = []

    while not rospy.is_shutdown():
        if too_close():
            kill_proxy("runner")

            x = random.uniform(1, 10)
            y = random.uniform(1, 10)
            theta = random.uniform(0, math.pi * 2)
            spawn_proxy(x, y, theta, "runner")

        # control the runner
        if time_since_last_runner_direction_change >= 2:
            runner_direction[0] = random.uniform(0, 1)
            runner_direction[1] = random.uniform(0, 1)
            time_since_last_runner_direction_change = 0
        control_message = Twist()
        control_message.linear.x = 1
        control_message.angular = runner_direction
        runner_publisher.publish(control_message)
        time_since_last_runner_direction_change += 1 / hz

        # control the hunter
        # ...

        rate.sleep()

if __name__ == '__main__':
    try:
        p1a()
    except rospy.ROSInterruptException:
        pass