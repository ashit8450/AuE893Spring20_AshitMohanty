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

    velocity_parameters.linear.x = 0
    velocity_publisher.publish(velocity_parameters)


def rotate(angular_speed, relative_angle, clockwise):

    velocity_parameters1 = Twist()
    velocity_parameters1.linear.x = 0
    velocity_parameters1.linear.y = 0
    velocity_parameters1.linear.z = 0

    velocity_parameters1.angular.x = 0
    velocity_parameters1.angular.y = 0

    if (clockwise):
        velocity_parameters1.angular.z = -abs(angular_speed)
    else:
        velocity_parameters1.angular.z = abs(angular_speed)

    current_angle = 0.0
    t0 = rospy.Time.now().to_sec()
    loop_rate = rospy.Rate(10)
    # velocity publisher
    velocity_publisher = rospy.Publisher(
        "/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_parameters1)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1-t0)
        loop_rate.sleep()
        if current_angle > relative_angle:
            rospy.loginfo("reached")
            break

    velocity_parameters1.angular.z = 0
    velocity_publisher.publish(velocity_parameters1)


def setDesiredOrientation(desired_angle_radians):
    relative_angle_radians = desired_angle_radians - yaw
    if relative_angle_radians < 0:
        clockwise = True
    else:
        clockwise = False
    rotate(np.deg2rad(30), abs(relative_angle_radians), clockwise)


def poseCallback(pose_message):
    global x
    global y
    global yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def moveGoal(goal_pose, distance_tolerance):

    global x, y, yaw
    x_goal = goal_pose.x
    y_goal = goal_pose.y

    velocity_message = Twist()

    # publisher
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    loop_rate = rospy.Rate(10)
    error = 0.0

    while True:

        kp = 0.5
        ki = 3.0

        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        velocity_message.linear.x = kp * distance
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0

        velocity_message.angular.x = 0
        velocity_message.angular.y = 0
        velocity_message.angular.z = ki * (math.atan2(y_goal-y, x_goal-x)-yaw)

        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

        if distance < distance_tolerance:
            print("end moveGoal")
            break

def square_closedloop():
    global x,y,yaw

    pose1 = Pose()
    pose2 = Pose()
    pose3 = Pose()
    pose4 = Pose()
    loop = rospy.Rate(1)

    # (5,5)
    pose1.x = 5
    pose1.y = 5
    pose1.theta = 0
    moveGoal(pose1,0.01)
    loop.sleep()
    setDesiredOrientation(np.deg2rad(0))

    # (8,5)
    pose2.x = 8
    pose2.y = 5
    pose2.theta = 0
    moveGoal(pose2,0.01)
    loop.sleep()
    rotate(np.deg2rad(40),np.deg2rad(90),False)

    # (8,8)
    pose3.x = 8
    pose3.y = 8
    pose3.theta = 0
    moveGoal(pose3,0.01)
    loop.sleep()

    # (8,5)
    pose4.x = 5
    pose4.y = 8
    pose4.theta = 0
    move(2,3, False)
    loop.sleep()
    setDesiredOrientation(np.deg2rad(0))

if __name__ == '__main__':
    try:
        # init node
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        # subscriber for turtlesim/Pose
        pose_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(pose_topic, Pose, poseCallback)

        square_closedloop()

    except rospy.ROSInterruptException:
        pass