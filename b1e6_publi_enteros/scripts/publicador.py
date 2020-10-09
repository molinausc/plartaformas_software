#! /usr/bin/env python

import rospy
from std_msgs.msg import Int32 


def publicador():
    pub = rospy.Publisher("b1e6_publi_enteros_canal1", Int32, queue_size=10)

    contador = 0
    while not rospy.is_shutdown():
        try:
            n = int(input("Dame un numero: "))
            pub.publish(n)
        except Exception:
            print("ERROR. Se ha de introducir un numero entero o convertible a entero.")


def callback(msg):
    print("\nSuma hecha en el suscriptor: %s" % msg.data)

def suscriptor():
    rospy.Subscriber("b1e7_susc_enteros_canal2", Int32, callback)


if  __name__ == '__main__':

    rospy.init_node('b1e6_publi_enteros') #por el momento no le metemos el argumento de anonymous = True

    try:
        suscriptor()
        publicador()
    except rospy.ROSInterruptException:
        print("Se para la ejecucion")

    
