#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

"""
anonymous = True, segundo argumento de init_node(arg[0],arg[1])
    Permite instanciar varias veces el mismo nodo, lo que hace es cambiar 
    el identificador del nodo para que no se reconozca como el mismo.
"""
rospy.init_node("nodo_basico")
pub = rospy.Publisher('/publicador_incremental',Int32,queue_size=1)
rate = rospy.Rate(2) # Frecuencia de 2Hz, que equivale a 0.5 seg

incremental = 0

while not rospy.is_shutdown(): # Infinito hasta "Crtl + c"
    incremental = incremental + 1
    pub.publish(incremental)
    print("Incremental:",incremental)
    rate.sleep() # espera el tiempo necesario hsata cumplir los 2 Hz que se configuraron antes