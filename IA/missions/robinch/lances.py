#/usr/bin/python

from missions.mission import Mission
import logging

class Lances(Mission):
    def __init__(self, robot, boardth):
        super(Lances, self).__init__(robot, boardth)
        self.name = 'Lances'
        self.pos = 0

    def go(self, msg):
        if (self.state == 'off' and msg.board == 'internal' and msg.name == 'beginLances'):
            self.state = 'on'
            self.pos = -0.900
            self.create_send_internal('forward', target=-0.897, axe='x')

        elif (self.state == 'on' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.asserv.launchBalls(1)
            self.state = "speed_lances"

        elif (self.state == 'alert' and msg.board == 'internal' and msg.name == 'freepath'): 
            self.asserv.launchBalls(1)
            self.state = 'speed_lances'

        elif self.state == "speed_lances":
            if (msg.board == 'asserv' and msg.name == 'doneLaunch'):
                self.asserv.stop()
                self.asserv.stopLaunch()
                self.asserv.odoBroadcastOff()
                self.state = 'off'
                self.create_send_internal('endLances')
           
            if (msg.board == 'asserv' and msg.name == 'doneBall'):
                self.pos = self.pos+0.05
                self.create_send_internal('forward', target=self.pos, axe='x')

            if (msg.board == 'internal' and msg.name == 'alert'):
                self.state = 'alert'
                self.asserv.stop()
                self.asserv.stopLaunch()
