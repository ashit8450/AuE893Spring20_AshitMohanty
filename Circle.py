#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math
import time

def plotcircle():
    velocity_variables = Twist()
    speed_z = 5
    speed_x = 3
    loop_rate = rospy.Rate(1)

    # publisher
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:
        velocity_variables.linear.x = speed_x
        velocity_variables.angular.x = 0

        velocity_variables.linear.y = 0
        velocity_variables.angular.y = 0

        velocity_variables.linear.z = 0
        velocity_variables.angular.z = speed_z

        print("velocity in x = %s" %velocity_variables.linear.x)
        print("velocity in z = %s" %velocity_variables.angular.z)

        velocity_publisher.publish(velocity_variables)
        loop_rate.sleep()

    # stop robot 
    velocity_variables.linear.x = 0
    velocity_variables.angular.z = 0
    print("velocity in x = %s" %velocity_variables.linear.x)
    print("velocity in z = %s" %velocity_variables.angular.z)
    velocity_publisher.publish(velocity_variables)


if __name__ == '__main__':
    try:
        # init node
        rospy.init_node('turtlesim_cleaner', anonymous=True)
        pose_topic = "/turtle1/pose"

        plotcircle()

    except rospy.ROSInterruptException:
        pass