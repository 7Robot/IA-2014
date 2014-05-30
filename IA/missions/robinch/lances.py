#/usr/bin/python

from missions.mission import Mission
import logging
from math import pi

class Lances(Mission):
    def __init__(self, robot, boardth):
        super(Lances, self).__init__(robot, boardth)
        self.name = 'Lances'
        self.pos = 0
        self.doneball = 0

    def go(self, msg):
        if (self.state == 'off' and msg.board == 'internal' and msg.name == 'beginLances'):
            self.state = 'on'
            self.pos = -0.835
            self.create_send_internal('forward', target=self.pos, axe='x')

        elif (self.state == 'on' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.create_send_internal('turn', target=pi)
            self.state = 'turn'

        elif (self.state == 'turn' and msg.board == 'internal' and msg.name == 'turn_done'): 
            self.asserv.launchBalls(5)
            self.doneball += 1
            self.state = "forw"
            
        elif (self.state == 'forw' and msg.name == 'doneLaunch'):
            self.pos += 0.05
            self.create_send_internal('forward', target=self.pos, axe='x')
            self.state = 'shoot'
            
        elif (self.state == 'turning' and msg.name == 'doneLaunch'):
            self.create_send_internal('turn', target=-11*pi/10)
            self.state = 'shoot'

        elif (self.state == 'turning2' and msg.name == 'doneLaunch'):
            self.create_send_internal('turn', target=11*pi/10)
            self.state = 'shoot'
            
        elif (self.state == 'shoot' and (msg.name == 'forward_done' or msg.name == 'turn_done')): 
            self.asserv.launchBalls((6-self.doneball)-1)
            self.doneball += 1
            if self.doneball == 4:
                self.state = "turning"
            elif (self.doneball == 2):
                self.state = "turning2"
            elif (self.doneball == 3):
                self.state = 'forw'
            else:
                self.state = 'ending'

        elif self.state == 'ending' and msg.name == 'doneLaunch':
            self.asserv.stopLaunch()
            self.create_send_internal('endLances')


        if (msg.board == "internal" and msg.name == "fin_du_match"):
            self.state = 'off'

