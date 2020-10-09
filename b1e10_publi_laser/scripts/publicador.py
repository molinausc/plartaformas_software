#! /usr/bin/env python

import rospy
import math
from std_msgs.msg import Int32 
from std_msgs.msg import String 
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

    print("La menor distancia encontrada es %d, que se encuentra a %d grados." % distanciaMin, angMin)
    pub.publish("La menor distancia encontrada es %d, que se encuentra a %d grados." % distanciaMin, angMin)

def suscriptor():
    rospy.Subscriber("scan", LaserScan, callback)


if  __name__ == '__main__':

    rospy.init_node('b1e10_publi_laser') #por el momento no le metemos el argumento de anonymous = True
    pub = rospy.Publisher("b1e10_publi_laser", String, queue_size=10)
    rate = rospy.Rate(2) 
    
    try:
        suscriptor()
    except rospy.ROSInterruptException:
        print("Se para la ejecucion")

    
