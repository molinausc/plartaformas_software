#!/usr/bin/env python

import rospy
from b1e4_publicador.msg import InfoPersonal

rospy.init_node("b1e4_publicador")
pub = rospy.Publisher('/b1e4_publicador',InfoPersonal,queue_size=1)
rate = rospy.Rate(2) 

datos = InfoPersonal()
datos.edad = 15
datos.nombre = "Molina"
datos.coeficiente = 2.56

while not rospy.is_shutdown(): 
    pub.publish(datos)
    rate.sleep() 