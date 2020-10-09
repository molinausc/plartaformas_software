#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32


def callback(msg):
    global contador,sumador,pub
    contador += 1
    sumador += msg.data
    print("Numero recibido: ", msg.data)
    if contador % 10 == 0:
        print("Sumatorio tras 10 numeros: ", sumador)
        pub.publish(sumador)
        sumador = 0


def suscriptor():
    rospy.Subscriber("b1e6_publi_enteros_canal1",Int32,callback)
    rospy.spin()


if __name__ == "__main__":
    try:
        rospy.init_node('b1e7_susc_enteros')
        pub = rospy.Publisher("b1e7_susc_enteros_canal2", Int32, queue_size=10)

        contador = 0
        sumador = 0

        suscriptor()
    except rospy.ROSInterruptException:
        print("Se para la ejecucion")

        