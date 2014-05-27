#/usr/bin/python

from missions.mission import Mission
import logging

class Capteurs(Mission):
    def __init__(self, robot, boardth):
        super(Capteurs, self).__init__(robot, boardth)
        self.name = 'Capteurs'

    def go(self, msg):
        logging.warn("Starting mission %s" % self.name)
        if self.state == 'on':
            if (msg.board == 'asserv' and msg.name == 'sick'):
                if msg.id == 1:
                    self.create_send_internal('alert', id=0)
                elif msg.id == 2:
                    self.create_send_internal('alert', id=1)
            elif (msg.board == 'asserv' and msg.name == 'freepath'):
                if msg.id == 1:
                    self.create_send_internal('freepath', id=0)
                elif msg.id == 2:
                    self.create_send_internal('freepath', id=1)
        elif self.state == 'off':
            self.state = 'on'
 
