#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

controls = [(1, 0), (1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (1, 0), (1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1),
            (-0.3, 1), (-0.3, 1), (-0.3, 1), (-0.3, -1), (-0.3, -1), (-0.3, -1), (-0.3, 1), (-0.3, 1), (-0.3, 1), (-0.3, -1), (-0.3, -1), (-0.3, -1)]

def p1a():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('turtle_controller', anonymous=True)
    rate = rospy.Rate(10)
    control_index = 0
    start_time = rospy.Time.now()
    while not rospy.is_shutdown():
        elapsed = (rospy.Time.now() - start_time).to_sec()
        control_index = int(elapsed // 1)
        if control_index < len(controls):
            control_message = Twist()
            control_message.linear.x = controls[control_index][0]
            control_message.linear.y = controls[control_index][1]
            pub.publish(control_message)
            control_index += 1
        rate.sleep()

if __name__ == '__main__':
    try:
        p1a()
    except rospy.ROSInterruptException:
        pass