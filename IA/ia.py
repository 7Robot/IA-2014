#/usr/bin/python

import logging
import os
from classmanager import class_loader
from missions.mission import Mission
from msg.msg import InternalMsg

class IA:
    def __init__(self, robot, boardth):
        self.robot = robot
        self.boardth = boardth 
        self.logging = logging

        self._load_all_missions(robot.name)

    def _load_all_missions(self, prefix):
        path = os.path.join(os.getcwd(), "missions", prefix)
        missions = set(class_loader(path))
        self.missions = []
        for mission in missions:
            if mission.__name__ != "Mission" and issubclass(mission, Mission):
                m = mission(self.robot, self.boardth)
                self.missions += [m]
                self.logging.warn('mission %s loaded ...' % m.__class__.__name__)


    def get_msg(self):
        return self.robot.queue.get(True)


    def run(self):
        self.robot.queue.put(InternalMsg("init"))
        while True:
            try:
                m = self.get_msg()
                logging.warn("msg:%s" % m.name)
                for mission in self.missions:
                    mission.go(m)

            except KeyboardInterrupt:
                break

