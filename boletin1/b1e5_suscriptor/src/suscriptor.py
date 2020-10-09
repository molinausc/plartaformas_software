#!/usr/bin/env python

import rospy
from b1e4_publicador.msg import InfoPersonal

def callback(msg):
    x = "Soy %s tengo %s anhos y un coeficiente de %s" % (msg.nombre, msg.edad, msg.coeficiente)
    print(x)

rospy.init_node('b1e5_suscriptor')

subscriber = rospy.Subscriber('/b1e4_publicador',InfoPersonal,callback)
rospy.spin()