#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

def callback(msg):
    print(msg.data)

rospy.init_node('paquete_suscriptor')

sub = rospy.Subscriber('/publicador_incremental',Int32,callback)
rospy.spin()