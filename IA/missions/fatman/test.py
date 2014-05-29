#/usr/bin/python

from missions.mission import Mission
import math

class Test(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)

    def go(self, msg):
        # look at this beautiful hack !
        if msg.board == 'asserv' and msg.name == 'blocked':
            msg.name = 'done'


        if msg.board == 'asserv' and msg.name == 'start':
            self.robot.color = msg.color
            self.create_send_internal('reset goto')
            self.create_send_internal('goto', position=(0.7, 0.05), angle=math.pi)
            self.state = 'sortie'
        elif self.state == 'sortie' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'prendre premier feu'
            self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre premier feu' and msg.name == 'caught':
            self.state = 'demi tour 1'
            self.create_send_internal('goto', position=(0.95, 0.05), angle=0)
        elif self.state == 'demi tour 1' and msg.name == 'goto done':
            self.state = 'fruits 1'
            self.create_send_internal('goto', position=(1.45, 0.04), angle=0)
        elif self.state == 'fruits 1' and msg.name == 'goto done':
            self.state = 'devant deuxième feu'
            self.create_send_internal('goto', position=(1.5, 0.51), angle=math.pi)
        elif self.state == 'devant deuxième feu' and msg.name == 'goto done':
            self.state = 'prendre deuxième feu'
            self.asserv.catch_arm(1 + (1 - self.robot.color))
        elif self.state == 'prendre deuxième feu' and msg.name == 'caught':
            self.state = 'pose feux'
            self.create_send_internal('goto', position=(1.64, 0.15), angle=0.8)
        elif self.state == 'pose feux' and msg.name == 'goto done':
            self.state = 'pose feu 1'
            self.asserv.pull_arm(1 + (1 - self.robot.color))
        elif self.state == 'pose feu 1' and msg.name == 'laid':
            self.state = 'demi tour feu 2'
            self.create_send_internal('goto', position=(1.56, 0.07), angle=0.8-math.pi)
        elif self.state == 'demi tour feu 2' and msg.name == 'goto done':
            self.asserv.pull_arm(1 + self.robot.color)
            self.state = 'pose feu 2'
        elif self.state == 'pose feu 2' and msg.name == 'laid':
            self.state = 'fruits 2 avant'
            self.create_send_internal('goto', position=(1.68, 0.30), angle=math.pi/2)
        elif self.state == 'fruits 2 avant' and msg.name == 'goto done':
            self.state = 'fruits 2'
            self.create_send_internal('goto', position=(1.68, 1.1), angle=math.pi/2)
        elif self.state == 'fruits 2' and msg.name == 'goto done':
            self.state = 'prendre troisième feu'
            self.asserv.catch_arm(1 + (1 - self.robot.color))
        elif self.state == 'prendre troisième feu' and msg.name == 'caught':
            self.state = 'avant quatrième feu'
            self.create_send_internal('goto', position=(1.68, 1.4), angle=-math.pi/2)
        elif self.state == 'avant quatrième feu' and msg.name == 'goto done':
            self.state = 'prendre quatrième feu'
            self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre quatrième feu' and msg.name == 'caught':
            self.state = 'vers foyer du milieu'
            self.create_send_internal('goto', position=(1.2, 1.25), angle=math.pi/2)
        elif self.state == 'vers foyer du milieu' and msg.name == 'goto done':
            pass

            self.state = 'convoyer'
            self.create_send_internal('convoyer')
        elif self.state == 'convoyer' and msg.name == 'convoyer done':
            self.state = 'filet'
            self.create_send_internal('filet')
        elif self.state == 'filet' and msg.board == 'internal' and msg.name == 'filet done':
            self.state = 'fini'
