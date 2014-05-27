#/usr/bin/python

from missions.mission import Mission
import logging
from math import pi

class Lances(Mission):
    def __init__(self, robot, boardth):
        super(Lances, self).__init__(robot, boardth)
        self.name = 'Lances'
        self.pos = 0

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

        elif (self.state == 'alert' and msg.board == 'internal' and msg.name == 'freepath'): 
            self.asserv.launchBalls(1)
            self.state = 'speed_lances'

        elif self.state == "speed_lances":
            if (msg.board == 'asserv' and msg.name == 'doneLaunch'):
                self.asserv.stop()
                self.asserv.stopLaunch()
                self.state = 'off'
                self.create_send_internal('endLances')
           
            elif (msg.board == 'asserv' and msg.name == 'doneBall'):
                self.create_send_internal('turn', target=pi)
                self.state = 'turn_speed'

        elif self.state == 'turn_speed' and msg.name == 'turn_done':
            if Mission.data['color'] == 'rouge':
                self.pos = self.pos - 0.05
            elif Mission.data['color'] == 'jaune':
                self.pos = self.pos + 0.05
            self.create_send_internal('forward', target=self.pos, axe='x')
            self.state = 'speed_lances'

