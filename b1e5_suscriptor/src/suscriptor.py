#!/usr/bin/env python

import rospy
from b1e4_publicador.msg import InfoPersonal

def callback(msg):
    print(msg)

rospy.init_node('b1e5_suscriptor')

subscriber = rospy.Subscriber('/b1e4_publicador',InfoPersonal,callback)
rospy.spin()