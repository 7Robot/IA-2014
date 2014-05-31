#!/usr/bin/python

from missions.mission import Mission

class Stop(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)

    def go(self, msg):
        if msg.board == 'internal' and msg.name == 'stop':
            self.asserv.block()
            self.robot.stopped = True
