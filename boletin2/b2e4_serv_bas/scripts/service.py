#! /usr/bin/env python

import rospy
import math
import time
from b2e4_serv_bas.srv import RespuestaServicio, RespuestaServicioResponse
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def callbackSus(msg):
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

    # Solo comtemplo la distancia frontal, no las laterales
    if dFrontal > 1:
        # avanzo frontal
        twist.linear.x = 0.5

    pub.publish(twist)

def callback(request):
    global yaSuscrito, tiempoEntrada, velEntrada
    print("Parametros recibidos:")
    tiempoEntrada = int(request.tiempoEntrada)
    velEntrada = float(request.velEntrada)
    print("Tiempo:",tiempoEntrada)
    print("Velocidad:",velEntrada)

    if not yaSuscrito:
        yaSuscrito = True
        # nos suscribimos al topic del scaner
        res = rospy.Subscriber("/scan", LaserScan, callbackSus)


    tret = RespuestaServicioResponse()
    tret.continua = True
    tret.tiempoMovimiento = 23

    return tret

yaSuscrito = False
tInicio = time.time()
tiempoEntrada = 0
velEntrada = 0
rospy.init_node("b2e4_serv_bas")
rate = rospy.Rate(0.5)
# lanzamos el servicio
servicio = rospy.Service("b2e4_serv_bas",RespuestaServicio,callback)
# preparamos para publicar la velocidad
pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
rospy.spin()