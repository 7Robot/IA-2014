#/usr/bin/python

from missions.mission import Mission
import logging
from msg.msg import Msg
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Wait for start'

    def go(self, msg, state):
        logging.warn("starting mission %s" % self.name)
        if state == 0:
            self.asserv.motion_pos(0.1, 0)
        elif state == 1:
            self.asserv.motion_angle(math.pi / 2)
        elif state == 2:
            self.asserv.motion_pos(0, 0)
        elif state == 3:
            self.asserv.motion_angle(0)

        return state + 1
