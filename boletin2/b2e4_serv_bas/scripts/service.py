#! /usr/bin/env python

import rospy
import math
import time
from b2e4_serv_bas.srv import RespuestaServicio, RespuestaServicioResponse
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

def resetGlobalVars():
    global subs, tInicio, tiempoEntrada, velEntrada, stop, tiempoRecorrido, continua
    subs = None
    tInicio = 0
    tiempoEntrada = 0
    velEntrada = 0
    stop = False
    tiempoRecorrido = 0
    continua = True

def callbackSus(msg):
    global pub, subs, velEntrada, tiempoEntrada, stop, tInicio, tiempoRecorrido, continua
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

    # comprobamos el tiempo pasado
    now = time.time()
    diff = now - tInicio
    cont = True
    if diff > tiempoEntrada:
        subs.unregister()
        stop = True
        subs = None
    else:
        # Solo comtemplo la distancia frontal, no las laterales
        if dFrontal > 1:
            # avanzo frontal
            twist.linear.x = velEntrada
        else: 
            subs.unregister()
            stop = True 
            cont = False
            subs = None

    tiempoRecorrido = diff
    continua = cont
        
    pub.publish(twist)

    # para controlar las frecuencias por consola y con el tiempo ver que se desuscribe y para de consumir recursos
    print("PRINT FROM SUSCRIBER",now) 

def callback(request):
    global subs, tiempoEntrada, velEntrada, stop, tInicio, tiempoRecorrido, continua

    # para poder seguir haciendo llamadas al servicio sin tener que reiniciarlo
    resetGlobalVars()

    print("Parametros recibidos:")
    tiempoEntrada = int(request.tiempoEntrada)
    velEntrada = float(request.velEntrada)
    print("Tiempo:",tiempoEntrada)
    print("Velocidad:",velEntrada)

    tInicio = time.time()

    tret = RespuestaServicioResponse()
    tret.continua = False
    tret.tiempoMovimiento = 0

    # comprobamos que la velocidad no sea muy alta
    if velEntrada >= 0.11 or velEntrada <= -0.11: # aproximo a 0.11 porque si introduces 0.1 te da algun decimal mas y da problemas
        return tret

    # comprobamos que no esta instanciado ya el suscriber
    if subs == None:
        # nos suscribimos al topic del scaner
        subs = rospy.Subscriber("/scan", LaserScan, callbackSus) 

    rate = rospy.Rate(1)
    while not stop:
        # para conctrolar las frecuencias por consola y ver que se ejecuta en paralelo al callback del suscriptor
        print("PRINT FROM SERVICE") 
        rate.sleep()

    tret.continua = continua
    tret.tiempoMovimiento = tiempoRecorrido

    return tret

subs = None
tInicio = 0
tiempoEntrada = 0
velEntrada = 0
stop = False
tiempoRecorrido = 0
continua = True
rospy.init_node("b2e4_serv_bas")
# lanzamos el servicio
servicio = rospy.Service("b2e4_serv_bas",RespuestaServicio,callback)
# preparamos para publicar la velocidad
pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
rospy.spin()