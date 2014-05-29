#/usr/bin/python

from missions.mission import Mission
import logging

class Capteurs(Mission):
    def __init__(self, robot, boardth):
        super(Capteurs, self).__init__(robot, boardth)
        self.name = 'Capteurs'

    def go(self, msg):
        if self.state == 'frontsick':
            if (msg.board == 'asserv' and msg.name == 'sick' and msg.id == 0):
                self.create_send_internal('alert', id='front')
             elif (msg.board == 'asserv' and msg.name == 'freepath' and msg.id == 0):
                self.create_send_internal('freepath', id='front')

        elif self.state == 'backsick':
            if (msg.board == 'asserv' and msg.name == 'sick' and msg.id == 1):
                self.create_send_internal('alert', id='back')
            elif (msg.board == 'asserv' and msg.name == 'freepath' and msg.id == 1):
                self.create_send_internal('freepath', id='back')

        elif self.state == 'on':
            if (msg.board == 'asserv' and msg.name == 'sick' and msg.id == 0):
                self.create_send_internal('alert', id='front')
            elif (msg.board == 'asserv' and msg.name == 'freepath' and msg.id == 0):
                self.create_send_internal('freepath', id='front')
            elif (msg.board == 'asserv' and msg.name == 'sick' and msg.id == 1):
                self.create_send_internal('alert', id='back')
            elif (msg.board == 'asserv' and msg.name == 'freepath' and msg.id == 1):
                self.create_send_internal('freepath', id='back')

                
        elif msg.name == 'beginSick':
            self.state = 'on'

        elif msg.name == 'backsick':
            self.state = 'backsick'

        elif msg.name =='frontsick':
            self.state = 'frontsick'

        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            self.state = 'off'

        elif msg.name == 'blindSick':
            self.state = 'off'
