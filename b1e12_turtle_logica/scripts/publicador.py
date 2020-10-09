#! /usr/bin/env python

import rospy
import math
from std_msgs.msg import Int32 , String
from sensor_msgs.msg import LaserScan

def callback(msg):
    global pub
    laserScan = msg 
    minAng = laserScan.angle_min
    maxAng = laserScan.angle_max
    incAng = laserScan.angle_increment
    rangos = laserScan.ranges
    maxRango = laserScan.range_max

    distanciaMin = maxRango
    posMin = 0
    for i in range(0,len(rangos)):
        r = rangos[i]
        if r < distanciaMin:
            distanciaMin = r 
            posMin = i
    
    radsMin = minAng + incAng * posMin
    angMin = math.degrees(radsMin)

    """ Toma de decisiones """
    """
    a. Si la distancia en frente del robot es mayor que 1 metro, el robot se debe mover
        hacia adelante
    b. Si la distancia en frente del robot es menor que 1 metro, el robot debe girar a la
        izquierda
    c. Si la distancia en la parte derecha del robot es menor que 1 metro, el robot
        girará hacia la izquierda
    d. Si la distancia en la parte izquierda del robot es menor que 1 metro, el robot
        girará hacia la derecha.robo
    """
  
    dFrontal = 0 #TODO: obtenerlo de alguna manera
    dDerecha = 0
    dIzquierda = 0

    if dFrontal > 1:
        # avanzo frontal
    elif dFrontal < 1:
        # giro izquierda
    elif dDerecha < 1:
        # giro izquierda
    elif dIzquierda < 1:
        # giro derecha
        


if  __name__ == '__main__':

    rospy.init_node('b1e11_publi_arco',anonymous=True) 
    pub = rospy.Publisher("b1e11_publi_arco", String, queue_size=1)
        
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.spin()

    
