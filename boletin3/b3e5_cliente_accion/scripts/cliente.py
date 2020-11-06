#!/usr/bin/env python

import rospy
import actionlib

from b3e5_accion_basico.msg import B3e5AccionGoal, B3e5AccionFeedback, B3e5AccionResult, B3e5AccionAction


def callback(state,result):
    global seguir
    seguir = False
    print("state",state)
    print("result",result)

def callbackFe(feedback):

    print("feedback",feedback.tiempo, feedback.proximidad)

seguir = True

rospy.init_node("b3e5_cliente_accion")

cli = actionlib.SimpleActionClient("/b3e5_accion_basico",B3e5AccionAction)
cli.wait_for_server()

goal = B3e5AccionGoal()
goal.tiempo = 3 
goal.velocidad = 0.05

cli.send_goal(goal, done_cb=callback, feedback_cb=callbackFe)
cli.get_state()

rate = rospy.Rate(1)

while seguir:
    print("esperando fin...")
    rate.sleep()
