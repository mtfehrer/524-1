#!/usr/bin/env python3
import math
import random
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Kill, Spawn

hunter_pos = [5, 5, 0]
runner_pos = [8, 8]

def too_close():
    x = hunter_pos
    y = runner_pos
    if ((x[1] - y[1]) ** 2 + (x[0] - y[0]) ** 2) ** 0.5 < 1:
        return True
    return False

def hunter_subscriber_callback(message):
    hunter_pos[0] = message.x
    hunter_pos[1] = message.y
    hunter_pos[2] = message.theta

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
    spawn_proxy(hunter_pos[0], hunter_pos[1], 0, "hunter")
    spawn_proxy(runner_pos[0], runner_pos[1], 0, "runner")

    time_since_last_runner_direction_change = 0
    runner_direction = 0

    while not rospy.is_shutdown():
        if too_close():
            kill_proxy("runner")
            theta = random.uniform(0, 2 * math.pi)
            spawn_proxy(random.uniform(1, 10), random.uniform(1, 10), theta, "runner")

        # control the runner
        if time_since_last_runner_direction_change >= 2:
            runner_direction = random.uniform(-1, 1)
            time_since_last_runner_direction_change = 0
        control_message = Twist()
        control_message.linear.x = 1
        control_message.angular.z = runner_direction
        runner_publisher.publish(control_message)
        time_since_last_runner_direction_change += 1 / hz

        # control the hunter
        dx = runner_pos[0] - hunter_pos[0]
        dy = runner_pos[1] - hunter_pos[1]
        desired_theta = math.atan2(dy, dx)
        angle_difference = desired_theta - hunter_pos[2]
        if angle_difference > math.pi:
            angle_difference -= 2 * math.pi
        elif angle_difference < -math.pi:
            angle_difference += 2 * math.pi
        hunter_message = Twist()
        hunter_message.linear.x = 1
        hunter_message.angular.z = 3 * angle_difference
        hunter_publisher.publish(hunter_message)

        rate.sleep()

if __name__ == '__main__':
    try:
        p1a()
    except rospy.ROSInterruptException:
        pass