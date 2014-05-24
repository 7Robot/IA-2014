#/usr/bin/python

from missions.mission import Mission
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Wait for start'

    def go(self, msg):
        if msg.board == 'internal' and msg.name == 'init':
            self.create_send_internal('goto', position=(0.7, 0.05), angle=math.pi)
            self.state = 'sortie'
        elif self.state == 'sortie' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'prendre premier feu'
            self.create_send_internal('filet')
            #self.asserv.catch_arm(2)

# y positif ==> on s'éloigne du bord original
