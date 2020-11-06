#!/usr/bin/env python

import rospy
import actionlib
import time
import math
from b3e5_accion_basico.msg import B3e5AccionAction, B3e5AccionFeedback, B3e5AccionResult
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class accion_basico(object):
    
    __realimentacion = B3e5AccionFeedback()
    __resultado = B3e5AccionResult()

    def __init__(self):
        self.__subs = None
        self.__tInicio = 0
        self.__tiempoEntrada = 0
        self.__velEntrada = 0
        self.__continua = True
        self.__stop = False
        self.__tiempoRecorrido = 0
        self.__distFro = 99
        self.__pub = rospy.Publisher("/mobile_base/commands/velocity", Twist, queue_size=1)
        self.__serv = actionlib.SimpleActionServer("server_accionbasico", B3e5AccionAction, self.__callbackServer, False)
        self.__serv.start()

    def __callbackServer(self,goal):
        # para poder seguir haciendo llamadas al servicio sin tener que reiniciarlo
        self.__resetGlobalVars() #TODO: aqui no se si es necesario

        print("Parametros recibidos:")
        self.__tiempoEntrada = int(goal.tiempo)
        self.__velEntrada = float(goal.velocidad)
        print("Tiempo:",self.__tiempoEntrada)
        print("Velocidad:",self.__velEntrada)

        self.__tInicio = time.time()

        validVel = True 
        # comprobamos que la velocidad no sea muy alta
        if self.__velEntrada >= 0.11 or self.__velEntrada <= -0.11: # aproximo a 0.11 porque si introduces 0.1 te da algun decimal mas y da problemas
            self.__resultado.resultado = 0
            self.__act_serv.set_aborted()
            validVel = False

        if validVel:
            # comprobamos que no esta instanciado ya el suscriber
            if self.__subs == None:
                # nos suscribimos al topic del scaner
                self.__subs = rospy.Subscriber("/scan", LaserScan, self.__callbackSus) 

            rate = rospy.Rate(1)
            while not self.__stop:
                #comprobamos si ha habido cancelacion del objetivo
                if self.__serv.is_preempt_requested():
                    print ("Cancelacion anticipada")
                    self.__serv.set_preempted()
                # para conctrolar las frecuencias por consola y ver que se ejecuta en paralelo al callback del suscriptor

                print("PRINT FROM ACTION") 
                rate.sleep()

            self.__resultado.resultado=self.__realimentacion.tiempo
            if self.__continua:
                print("fin bonito")
                self.__serv.set_succeeded(self.__resultado)
            else:
                print("fin feo")
                self.__serv.set_aborted(self.__resultado)

            
    def __resetGlobalVars(self):
        self.__subs = None
        self.__tInicio = 0
        self.__tiempoEntrada = 0
        self.__velEntrada = 0
        self.__stop = False
        self.__tiempoRecorrido = 0
        self.__continua = True


    def __callbackSus(self, msg):
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
        diff = now - self.__tInicio
        if diff > self.__tiempoEntrada:
            self.__subs.unregister()
            self.__stop = True
            self.__subs = None
        else:
            # Solo comtemplo la distancia frontal, no las laterales
            if dFrontal > 1:
                # avanzo frontal
                twist.linear.x = self.__velEntrada
            else: 
                self.__subs.unregister()
                self.__stop = True 
                self.__continua = False
                self.__subs = None

        self.__tiempoRecorrido = diff
        self.__distFro = dFrontal
            
        #publicamos la velocidad del robot
        self.__pub.publish(twist)

        # mandamos feedback de como va el proceso
        self.__realimentacion.tiempo = self.__tiempoRecorrido
        self.__realimentacion.proximidad = self.__distFro
        self.__serv.publish_feedback(self.__realimentacion)

        # para controlar las frecuencias por consola y con el tiempo ver que se desuscribe y para de consumir recursos
        print("PRINT FROM SUSCRIBER",now) 


rospy.init_node('b3e5_accion_simple')
accion_basico()
rospy.spin()