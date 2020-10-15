#!/usr/bin/env python
import rospy
from std_srvs.srv import Empty,EmptyResponse

def my_callback(request):

    rate=rospy.Rate(0.5)
    print ('esto es una prueba de como funcioan servcio')
    for i in range (0,10,1):
        segundos=i*2.0
        print ('han transcurridos ',segundos,' segundos')
        rate.sleep()
    return EmptyResponse()



rospy.init_node('nodo_servidor_servicio_roberto')
my_service=rospy.Service('/servicio_roberto',Empty,my_callback)
rospy.spin()