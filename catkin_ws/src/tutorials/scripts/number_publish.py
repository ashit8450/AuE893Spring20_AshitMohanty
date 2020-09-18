#!/usr/bin/env python

import rospy
from std_msgs.msg import Int64

if __name__ == '__main__':
     
     rospy.init_node("number_publisher")
     
     pub = rospy.Publisher("/number", Int64, queue_size=10)

     rate = rospy.Rate(1)
    
     while not rospy.is_shutdown():
           msg = Int64()
           msg.data = 3
           
           pub.publish(msg)

           rospy.loginfo(msg)
           rate.sleep()

           



