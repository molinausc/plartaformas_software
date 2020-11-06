#!/usr/bin/env python

import rospy
import math
import actionlib

from turtlesim.srv import Spawn, SpawnRequest, SpawnResponse, Kill, KillRequest, KillResponse
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

from ejer3.msg import ServerAccionGoal, ServerAccionFeedback, ServerAccionResult, ServerAccionAction


def callback(state,result):

def callbackFe(feedback):


seguir = True

rospy.init_node("ejer31_client")

cli = actionlib.SimpleActionClient("/b3e5_accion_basico",B3e5AccionAction)
cli.wait_for_server()

goal = ServerAccionGoal()
goal.tiempo = 3 
goal.velocidad = 0.05

cli.send_goal(goal, done_cb=callback, feedback_cb=callbackFe)
cli.get_state()

rate = rospy.Rate(4)

while seguir:
    print("esperando fin...")
    rate.sleep()