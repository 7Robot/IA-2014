#/usr/bin/python

from missions.mission import Mission
import logging

class Peintures(Mission):
    def __init__(self, robot, boardth):
        super(Peintures, self).__init__(robot, boardth)
        self.name = 'Peintures'

    def go(self, msg):
        if (self.state == 1 and msg.board == 'internal' and msg.name == 'beginmatch'):
            logging.warn("starting mission %s" % self.name)
            self.asserv.distRot(1, 0)
            self.state = 2
        if self.state == 2:
            if (msg.board == 'internal' and msg.name == 'alert'):
                self.asserv.stop()
                #determiner la distance a l'objet
            elif (msg.board == 'asserv' and msg.name == 'freepath'):
                self.asserv.distRot(0,0)
                #envoyer la consigne a l'objet
            elif (msg.board == 'asserv' and msg.name == 'done'):
                self.state = 3

