#/usr/bin/python

from missions.mission import Mission
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Wait for start'

    def go(self, msg):
        if msg.board == 'internal' and msg.name == 'init':
            self.asserv.setPos(0, 0, math.pi)
            self.create_send_internal('goto', position=(0.7, 0.05), angle=math.pi)
            self.state = 'sortie'
        elif self.state == 'sortie' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'prendre premier feu'
            self.asserv.catch_arm(2)
        elif self.state == 'prendre premier feu' and msg.board == 'asserv' and msg.name == 'caught':
            self.state = 'demi tour 1'
            self.create_send_internal('goto', position=(0.7, 0.06), angle=0)
        elif self.state == 'demi tour 1' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'fruits 1'
            self.create_send_internal('goto', position=(1.5, 0.06), angle=0)
        elif self.state == 'fruits 1' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'aller au mammouth'
            self.create_send_internal('goto', position=(0.7, 0.7), angle=math.pi)
        elif self.state == 'aller au mammouth' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'fini'
            self.create_send_internal('filet')

# y positif ==> on s'éloigne du bord original
