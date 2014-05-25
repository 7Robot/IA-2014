#/usr/bin/python

from missions.mission import Mission
import logging

class Lances(Mission):
    def __init__(self, robot, boardth):
        super(Lances, self).__init__(robot, boardth)
        self.name = 'Lances'
        self.balls = 0

    def go(self, msg):
        if (self.state = 'off' and msg.board == 'internal' and msg.name == 'beginlances'):
            self.state = 'on'
            self.create_send_internal('forward', target=0.62, axe='x')

        elif (self.state == 'on' and msg.board == 'internal' and msg.name == 'forward_done'):
            self.asserv.odoBroadcastOn()
            self.asserv.speed(0.03, 0.1, 0.1)
            self.asserv.launchBalls(1)
            self.state = "speed_lances"

        elif ((self.state = 'speed_lances' or self.state = 'speed_lances_2') \
                    and msg.board == 'internal' and msg.name == 'alert'):
            self.asserv.stop()
            self.asserv.stopLaunch()
            self.state = 'alert'

        elif (self.state = 'alert' and msg.board == 'internal' and msg.name == 'freepath'): 
            self.asserv.speed(0.03, 0.1, 0.1)
            self.asserv.launchBalls(1)
            self.state = 'speed_lances'

        elif self.state == "speed_lances":
            if (msg.board == 'asserv' and msg.name == 'doneLaunch'):
                self.asserv.stop()
                self.asserv.stopLaunch()
                self.asserv.odoBroadcastOff()
                self.state = 'off'
                self.create_send_internal('endLances')

            if (msg.board == 'asserv' and msg.name == 'pos' and abs(msg.x) > 0.90):
                self.asserv.stop()
                self.asserv.stopLaunch()
                self.asserv.odoBroadcastOff()
                self.state = 'off' 
                self.create_send_internal('endLances')


