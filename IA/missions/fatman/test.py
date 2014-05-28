#/usr/bin/python

from missions.mission import Mission
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)

    def go(self, msg):
        if msg.board == 'asserv' and msg.name == 'start':
            self.robot.color = msg.color
            self.asserv.setPos(0, 0, math.pi)
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
            self.asserv.push_arm(1 + self.robot.color)
        elif self.state == 'lacher 1' and msg.name == 'laid':
            self.state = 'fini'


# y positif ==> on s'éloigne du bord original
