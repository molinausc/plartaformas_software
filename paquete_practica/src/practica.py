#!/usr/bin/env python
import rospy

"""
anonymous = True, segundo argumento de init_node(arg[0],arg[1])
    Permite instanciar varias veces el mismo nodo, lo que hace es cambiar 
    el identificador del nodo para que no se reconozca como el mismo.
"""
rospy.init_node("nodo_basico")
rate = rospy.Rate(2) # Frecuencia de 2Hz

incremental = 0

while not rospy.is_shutdown(): # Infinito hasta "Crtl + c"
    incremental = incremental + 1
    print("Incremental:",incremental)
    rate.sleep() # espera el tiempo necesario hsata cumplir los 2 Hz que se configuraron antes