#! /usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

def callback(msg):
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    z = msg.pose.pose.position.z
    print("La posicion recibida por odometria es: ",(x,y,z))

rospy.init_node('b1e9_susc_odom')

subscriber = rospy.Subscriber('/odom',Odometry,callback)
rospy.spin()