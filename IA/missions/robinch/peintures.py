#/usr/bin/python

from missions.mission import Mission
import logging

class Peintures(Mission):
    def __init__(self, robot, boardth):
        super(Peintures, self).__init__(robot, boardth)
        self.name = 'Peintures'

    def go(self, msg):
        if (self.state == 'off' and msg.board == 'internal' and msg.name == 'beginPeintures'):
            self.state = 'on'
            self.create_send_internal('forward', target=1, axe='x')

        elif (self.state == 'on' and msg.board == 'internal' and msg.name == 'forward_done'):
            pass

