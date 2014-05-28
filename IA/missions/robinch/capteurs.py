#/usr/bin/python

from missions.mission import Mission
import logging

class Capteurs(Mission):
    def __init__(self, robot, boardth):
        super(Capteurs, self).__init__(robot, boardth)
        self.name = 'Capteurs'

    def go(self, msg):
        if self.state == 'on':
            if (msg.board == 'asserv' and msg.name == 'sick'):
                if msg.id == 0:
                    self.create_send_internal('alert', id='front')
                elif msg.id == 1:
                    self.create_send_internal('alert', id='back')
            elif (msg.board == 'asserv' and msg.name == 'freepath'):
                if msg.id == 0:
                    self.create_send_internal('freepath', id='front')
                elif msg.id == 1:
                    self.create_send_internal('freepath', id='back')
        elif self.state == 'off' and msg.name == 'beginSick':
            self.state = 'on'

        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            self.state = 'off'

        elif self.state == 'on' and msg.name == 'blindSick':
            self.state = 'off'
