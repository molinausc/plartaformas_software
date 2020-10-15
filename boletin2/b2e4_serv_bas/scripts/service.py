#! /usr/bin/env python

import rospy
import rospkg
from b2e4_serv_bas.srv import RespuestaServicio, RespuestaServicioResponse

def callback(request):
    print("Parametros recibidos:")
    tiempoEntrada = request.tiempoEntrada
    velEntrada = request.velEntrada
    print("Tiempo:",tiempoEntrada)
    print("Velocidad:",velEntrada)

    tret = RespuestaServicioResponse()
    tret.continua = True
    tret.tiempoMovimiento = 23

    return tret


rospy.init_node("b2e4_serv_bas")
rate = rospy.Rate(0.5)
servicio = rospy.Service("b2e4_serv_bas",RespuestaServicio,callback)
