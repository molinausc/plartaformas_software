#!/usr/bin/env python

import rospy
import math

from turtlesim.srv import Spawn, SpawnRequest, SpawnResponse, Kill, KillRequest, KillResponse
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from ejer2.srv import RespuestaServicio, RespuestaServicioRequest, RespuestaServicioResponse

def crearTortuga(nombre,x,y,theta):

    rospy.wait_for_service('/spawn')
    servicio = rospy.ServiceProxy('/spawn',Spawn)

    arg = SpawnRequest()
    arg.x = float(x)
    arg.y = float(y)
    arg.theta = float(theta)
    arg.name = str(nombre)

    result = servicio(arg)

    print("Tortuga creada:",result.name)

def borrarTortuga(nombre):

    rospy.wait_for_service('/kill')
    servicio = rospy.ServiceProxy('/kill',Kill)

    arg = KillRequest()
    arg.name = str(nombre)

    result = servicio(arg)
    print("Tortuga borrada:",nombre)

def callbackPresa(msg):
    global presa_x, presa_y, presa_theta, presa_linear, presa_angular, recibi_presa
    presa_x = msg.x
    presa_y = msg.y
    presa_theta = msg.theta
    presa_linear = msg.linear_velocity
    presa_angular = msg.angular_velocity

    recibi_presa = True

def callbackDepredador(msg):
    global depredador_x, depredador_y, depredador_theta, depredador_linear, depredador_angular, recibi_depredador
    depredador_x = msg.x
    depredador_y = msg.y
    depredador_theta = msg.theta
    depredador_linear = msg.linear_velocity
    depredador_angular = msg.angular_velocity

    recibi_depredador = True

def callbackService(request):
    umbral = int(request.distancia)

    crearTortuga("presa",5,10,3.1416)
    crearTortuga("depredador",4.9,5,6)
    borrarTortuga("turtle1")

    # nos conectamos al publicador de velocidades
    pubPresaVel = rospy.Publisher("/presa/cmd_vel", Twist)
    pubDepredadorVel = rospy.Publisher("/depredador/cmd_vel", Twist)

    susPresa = rospy.Subscriber('/presa/pose',Pose,callbackPresa)
    susDepredador = rospy.Subscriber('/depredador/pose',Pose,callbackDepredador)

    rate = rospy.Rate(4)
    # esperamos a tener los primeros datos de las tortugas
    while (not recibi_presa and not recibi_depredador):
        rate.sleep()

    # calculo primera distancia
    xb = presa_x - depredador_x 
    yb = presa_y - depredador_y 
    distancia = math.sqrt(math.pow(xb,2)+math.pow(yb,2))

    while distancia>umbral and not rospy.is_shutdown():
        vel_linear_x = 1.5 * math.sqrt(math.pow((presa_x - depredador_x),2) + math.pow((presa_y - depredador_y),2))
        vel_angular_z = 4 * (math.atan2(presa_y - depredador_y, presa_x - depredador_x) - depredador_theta)

        xb = presa_x - depredador_x 
        yb = presa_y - depredador_y 
        distancia = math.sqrt(math.pow(xb,2)+math.pow(yb,2))

        twistPresa = Twist()
        twistPresa.linear.x = float(0.3)
        twistPresa.angular.z = float(0.08)

        twistDepredador = Twist()
        twistDepredador.linear.x = float(vel_linear_x * 0.91)
        twistDepredador.angular.z = float(vel_angular_z)

        pubPresaVel.publish(twistPresa)
        pubDepredadorVel.publish(twistDepredador)   

        rate.sleep()  

    # detenemos el depredador
    twistDep = Twist()
    twistDep.linear.x = float(0)
    twistDep.angular.z = float(0)
    pubDepredadorVel.publish(twistDep)

    tret = RespuestaServicioResponse()
    # tomo correcto o no si se ha aproximado lo suficiente
    tret.correcto = distancia<umbral

    return tret


recibi_presa = False
recibi_depredador = False

rospy.init_node("ejer2")

rate = rospy.Rate(4)
# lanzamos el servicio
servicio = rospy.Service("ejer2_service",RespuestaServicio,callbackService)

rospy.spin()