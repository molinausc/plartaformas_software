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

    men = "La menor distancia encontrada es %f, que se encuentra a %f grados." % (distanciaMin, angMin)
    print(men)
    pub.publish(men)


if  __name__ == '__main__':

    rospy.init_node('b1e10_publi_laser',anonymous=True) 
    pub = rospy.Publisher("b1e10_publi_laser", String, queue_size=1)
        
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.spin()

    
