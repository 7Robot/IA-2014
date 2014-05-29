#/usr/bin/python

from missions.mission import Mission
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)

    def go(self, msg):
        # look at this beautiful hack !
        if msg.board == 'asserv' and msg.name == 'blocked':
            msg.name = 'goto done'
            msg.board = 'internal'

        if msg.board == 'asserv' and msg.name == 'start':
            self.robot.color = msg.color
            self.create_timer(3, 'timer start')
            self.create_timer(92, 'funny action')
            self.state = 'waiting for start'
        elif msg.name == 'timer start' and self.state == 'waiting for start':
            self.create_send_internal('reset goto')
            self.create_send_internal('goto', position=(0.7, 0.05), angle=math.pi)
            self.state = 'sortie'
        elif self.state == 'sortie' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'prendre premier feu'
            self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre premier feu' and msg.name == 'caught':
            self.state = 'demi tour 1'
            self.create_send_internal('goto', position=(1.62, 0.14), angle=0.8-math.pi)
        elif self.state == 'demi tour 1' and msg.name == 'goto done':
            self.state = 'lacher 1'
            self.asserv.pull_arm(1 + self.robot.color)
        elif self.state == 'lacher 1' and msg.name == 'laid':
            self.state = 'fini'


# y positif ==> on s'éloigne du bord original
