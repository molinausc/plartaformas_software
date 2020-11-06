#!/usr/bin/env python

import rospy
import math
import actionlib

from turtlesim.srv import Spawn, SpawnRequest, SpawnResponse, Kill, KillRequest, KillResponse
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from ejer2.srv import RespuestaServicio, RespuestaServicioRequest, RespuestaServicioResponse