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

    men = "\nLa menor distancia encontrada es %f, que se encuentra a %f grados." % (distanciaMin, angMin)
    print(men)
    pub.publish(men)

    """
    Para indicar el arco mas libre voy a aplicar el siguiente razonamiento, tomare el valor de maximo rango y lo ire buscando dentro de grupos de 20 elementos (20 elegido arbitrariamente), 
    el grupo de 20 que mas veces lo contenga sera el mas libre.
    """
    cSeccion = 20
    posIni = 0
    posFin = 19
    maxi = 0
    arco = [0,0]
    for i in range(cSeccion,len(rangos)):
        sec = rangos[i-cSeccion:i]
        suma = sum(map(lambda x: x==maxRango,sec))
        if suma > maxi:
            maxi = suma
            arco = [i-cSeccion,i]

    # No publico el arco, solo lo muestro ya que no se especifica nada a mayores de calcularlo
    if arco[0] == 0 and arco[1] == 0:
        print("No se ha podido detectar en ningun punto del rango una distancia mayor al limite del laser.")
    else:
        arcoDeg = [math.degrees(minAng+incAng*arco[0]),math.degrees(minAng+incAng*arco[1])]
        print("El arco mas libre esta en la posicion:", arco, "Para los grados:", arcoDeg)
        


if  __name__ == '__main__':

    rospy.init_node('b1e11_publi_arco',anonymous=True) 
    pub = rospy.Publisher("b1e11_publi_arco", String, queue_size=1)
        
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.spin()

    
