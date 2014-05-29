#/usr/bin/python

from missions.mission import Mission
import logging
from math import pi

class Peintures(Mission):
    def __init__(self, robot, boardth):
        super(Peintures, self).__init__(robot, boardth)
        self.name = 'Peintures'

    def go(self, msg):
        if (self.state == 'off' and msg.board == 'internal' and msg.name == 'beginPeintures'):
            self.state = 'on'
            self.create_send_internal('turn', target=-pi/2)

        elif (self.state == 'on' and msg.board == 'internal' and msg.name =='turn_done'):
            self.create_send_internal('backsick')
            self.create_send_internal('forward', target=0.750, axe='y')
            self.state = 'before'
            
        elif (self.state == 'before' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.create_send_internal('turn', target=-pi/2)
            self.create_send_internal('blindSick')
            self.state = 'pinage'

        elif (self.state == 'pinage' and msg.board == 'internal' and msg.name =='turn_done'):
            self.create_timer(3.0, 'end_pinage')
            self.create_send_internal('forward', target=1, axe='y')
            
        elif (self.state == 'pinage' and msg.board == 'internal' and msg.name == 'end_pinage'):
            self.asserv.stop()
            self.state = 'ackbar'
            self.create_send_internal('frontsick')
            
        elif (self.state == 'ackbar' and msg.board == 'asserv' and msg.name =='done'):
            self.create_send_internal('forward', target=0.950, axe='y')
            
        elif (self.state == 'ackbar' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.create_send_internal('turn', target=-pi/2)
            self.create_send_internal('beginSick')
            
        elif (self.state == 'ackbar' and msg.board == 'internal' and msg.name =='turn_done'):
            self.create_send_internal('endPeintures')
            self.state = 'off'
            
        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            self.state = 'off'

