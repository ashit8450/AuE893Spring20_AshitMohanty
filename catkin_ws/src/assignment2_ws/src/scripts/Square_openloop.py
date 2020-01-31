#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
import numpy as np

X_min = 0.0
Y_min = 0.0
X_max = 11.0
Y_max = 11.0

x=0
y=0
yaw=0

def move(speed, distance, isForward):
    velocity_parameters = Twist()

    velocity_parameters.linear.y = 0
    velocity_parameters.linear.z = 0

    velocity_parameters.angular.x = 0
    velocity_parameters.angular.y = 0
    velocity_parameters.angular.z = 0

    if (isForward):
        velocity_parameters.linear.x = abs(speed)
    else:
        velocity_parameters.linear.x = -abs(speed)

    t0 = rospy.Time.now().to_sec()
    current_distance = 0
    loop_rate = rospy.Rate(10)

    # velocity publisher
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_parameters)
        t1 = rospy.Time.now().to_sec()
        current_distance = speed * (t1-t0)
        loop_rate.sleep()

        if not (current_distance < distance):
            rospy.loginfo("reached")
            break


def rotate(angular_speed, relative_angle, clockwise):

    velocity_parameters_1 = Twist()
    velocity_parameters_1.linear.x = 0
    velocity_parameters_1.linear.y = 0
    velocity_parameters_1.linear.z = 0

    velocity_parameters_1.angular.x = 0
    velocity_parameters_1.angular.y = 0

    if (clockwise):
        velocity_parameters_1.angular.z = -abs(angular_speed)
    else:
        velocity_parameters_1.angular.z = abs(angular_speed)

    current_angle = 0.0
    t0 = rospy.Time.now().to_sec()
    loop_rate = rospy.Rate(10)
    # velocity publisher
    velocity_publisher = rospy.Publisher(
        "/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_parameters_1)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1-t0)
        loop_rate.sleep()
        if current_angle > relative_angle:
            rospy.loginfo("reached")
            break


def square_openloop():
    loop = rospy.Rate(0.5)

    move(0.2, 2.0, True)
    rotate(0.2, np.deg2rad(90), False)
    loop.sleep()
    move(0.2, 2.0, True)

    rotate(0.2, np.deg2rad(90), False)
    loop.sleep()
    move(0.2, 2.0, True)
    rotate(0.2, np.deg2rad(90), False)
    loop.sleep()
    move(0.2, 2.0, True)

if __name__ == '__main__':
    try:
        # init node
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        square_openloop()

    except rospy.ROSInterruptException:
        pass