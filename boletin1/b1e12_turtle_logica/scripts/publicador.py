#! /usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

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

    # Voy a partir en tres partes el rango de medidas del laser y lo utilizare para identificar cada zona del robot (frontal, izquierda y derecha)    
    partes = len(rangos)/3

    # Minima distancia en cada zona
    dDerecha = maxRango 
    dFrontal = maxRango 
    dIzquierda = maxRango
    for i in range(0,len(rangos)):
        if i < math.floor(partes): 
            if rangos[i] < dDerecha:
                dDerecha = rangos[i]
        elif i < math.floor(partes)*2:
            if rangos[i] < dFrontal:
                dFrontal = rangos[i]
        else:
            if rangos[i] < dIzquierda:
                dIzquierda = rangos[i]

    #Creamos el objeto del request
    twist = Twist()
    twist.linear.x = 0.0
    twist.linear.y = 0.0
    twist.linear.z = 0.0
    twist.angular.x = 0.0
    twist.angular.y = 0.0
    twist.angular.z = 0.0

    if dFrontal > 1:
        # avanzo frontal
        twist.linear.x = 0.5
    elif dFrontal < 1: 
        # giro izquierda
        twist.angular.z = 2*math.pi/4 
    elif dDerecha < 1:
        # giro izquierda
        twist.angular.z = 2*math.pi/4
    elif dIzquierda < 1:
        # giro derecha
        twist.angular.z = -2*math.pi/4

    """ 
    No avanzo en el giro porque no se especifica concretamente y presupongo que es por usar distintas opciones de ROS 
    Ademas publico de 1 en 1 basandome en la frecuencia con la que recibo las mediciones de scan. Por eso no uso el Rate()
    """
        
    pub.publish(twist)


if  __name__ == '__main__':

    rospy.init_node('b1e11_publi_arco',anonymous=True) 
    pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.spin()


