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
            self.pos = -0.880
            self.create_send_internal('forward', target=self.pos, axe='x')

        elif (self.state == 'on' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.create_send_internal('turn', target=pi)
            self.state = 'turn'

        elif (self.state == 'turn' and msg.board == 'internal' and msg.name == 'turn_done'): 
            self.asserv.launchBalls(1)
            self.state = "speed_lances"
            self.create_send_internal('forward', target=self.pos+0.05, axe='x')

        elif (self.state == 'alert' and msg.board == 'internal' and msg.name == 'freepath'): 
            self.asserv.launchBalls(1)
            self.state = 'speed_lances'

        elif self.state == "speed_lances":              
            if msg.name == 'forward_done':
                self.create_send_internal('turn', target=pi)
                self.state = 'turn_speed'
            elif msg.name == 'doneLaunch':
                self.state = 'ending'
                
        elif self.state == 'turn_speed':
            if msg.name == 'turn_done':
                self.create_send_internal('forward', target=self.pos+0.10, axe='x')
                self.state = 'speed_lances'
            elif msg.name == 'doneLaunch':
                self.state = 'ending'

        elif self.state == 'ending' and msg.name == 'done':
            self.asserv.stopLaunch()
            self.create_send_internal('endLances')


        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            self.state = 'off'

