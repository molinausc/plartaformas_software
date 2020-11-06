#!/usr/bin/env python

import rospy
import actionlib
import time

from actionlib.msg import TestAction,TestFeedback,TestResult
from std_msgs.msg import Empty

class accion_simple(object):

    __realimentacion = TestFeedback() 
    __resultado = TestResult() 

    def __init__(self):

        self.__act_serv=actionlib.SimpleActionServer("serv_acc_basico",TestAction,self.goal_callback,False)
        self.__act_serv.start()
    
    def goal_callback(self,goal):
    
        success=True #por defecto se asume que la actividad se ejecuta bien
        
        feedback=0

        tiempo_objetivo=goal.goal
        print ("el tiempo fijado como objetivo es: ",tiempo_objetivo)
        rate=rospy.Rate(1)

        t=time.time()
        delta=-1

        while delta<tiempo_objetivo:

            #comprobamos que no se ha producido una pre-cancelacion de objetivo....
            if self.__act_serv.is_preempt_requested():
                print ("se ha producido una cancelacion anticipada .... ")
                self.__act_serv.set_preempted()
                success=False
                break

            t2=time.time()
            delta=t2-t
            print ("tiempo transcurrido: ",delta)
            self.__realimentacion.feedback=(int)(delta)
            self.__act_serv.publish_feedback(self.__realimentacion)
            rate.sleep()


        if success:
            self.__resultado.result=self.__realimentacion.feedback
            self.__act_serv.set_succeeded(self.__resultado)
            
        else:
            self.__resultado.result=self.__realimentacion.feedback
            self.__act_serv.set_aborted()

            

        

rospy.init_node('servidor_accion_muy_basico')
accion_simple()
rospy.spin()