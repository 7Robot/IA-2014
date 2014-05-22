#/usr/bin/python

from missions.mission import Mission
import logging

class Lances(Mission):
    def __init__(self, robot, boardth):
        super(Lances, self).__init__(robot, boardth)
        self.name = 'Lances'

    def go(self, msg):
        if (self.state == 'rouge' and msg.board == 'internal' and msg.name == 'beginmatch'):
            logging.warn("starting mission %s" % self.name)
            self.create_send_internal('forward', {'target':0.62, 'axe':'x', 'mission':self.name})

        elif (self.state == "" % self.name):
            self.asserv.speed(0.05, 0.1, 0.1)
            self.asserv.launchBalls(5)
            self.state = "speed_lances"

        elif (self.state == "speed_lances"):
            if (msg.board == 'internal' and msg.name == 'alert'):

