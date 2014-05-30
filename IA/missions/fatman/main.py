#!/usr/bin/python

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
            self.create_timer(85, 'stop')
            self.create_timer(75, 'the end is near')
            self.state = 'waiting for start'
        elif msg.name == 'timer start' and self.state == 'waiting for start':
            self.create_send_internal('reset goto')
            self.create_send_internal('goto', position=(0.7, 0.05), angle=math.pi)
            self.state = 'sortie'
        elif self.state == 'sortie' and msg.board == 'internal' and msg.name == 'goto done':
            self.state = 'prendre premier feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre premier feu' and msg.name == 'caught':
            self.state = 'devant deuxième feu'
            self.create_send_internal('goto', position=(0.8, 0.22), angle=math.pi/2)
        elif self.state == 'devant deuxième feu' and msg.name == 'goto done':
            self.state = 'prendre deuxième feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(2 - self.robot.color)
        elif self.state == 'prendre deuxième feu' and msg.name == 'caught':
        # POSE DES FEUX
            self.state = 'pose feux'
            if not self.robot.stopped:
                self.asserv.raise_arm(2 - self.robot.color)
            self.create_send_internal('goto', position=(1.64, 0.15), angle=0.7)
        elif self.state == 'pose feux' and msg.name == 'goto done':
            self.state = 'pose feu 1'
            if not self.robot.stopped:
                self.asserv.push_arm(2 - self.robot.color)
        elif self.state == 'pose feu 1' and msg.name == 'laid':
            self.state = 'demi tour feu 2'
            if not self.robot.stopped:
                self.asserv.raise_arm(1 + self.robot.color)
            self.create_send_internal('goto', position=(1.56, 0.07), angle=0.8-math.pi)
        elif self.state == 'demi tour feu 2' and msg.name == 'goto done':
            if not self.robot.stopped:
                self.asserv.pull_arm(1 + self.robot.color)
            self.state = 'pose feu 2'
        elif self.state == 'pose feu 2' and msg.name == 'laid':
        # FIN POSE FEUX
            self.state = 'devant troisième feu'
            self.create_send_internal('goto', position=(1.5, 0.52), angle=math.pi)
        elif self.state == 'devant troisième feu' and msg.name == 'goto done':
            self.state = 'prendre troisième feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(1 + (1 - self.robot.color))
        elif self.state == 'prendre troisième feu' and msg.name == 'caught':
            self.state = 'devant quatrième feu'
            self.create_send_internal('goto', position=(1.68, 1.135), angle=math.pi/2)
        elif self.state == 'devant quatrième feu' and msg.name == 'goto done':
            self.state = 'prendre quatrième feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(2 - self.robot.color)
        elif self.state == 'prendre quatrième feu' and msg.name == 'caught':
        # FOYER MILIEU
            self.state = 'vers foyer du milieu'
            if not self.robot.stopped:
                self.asserv.raise_arm(1 + self.robot.color)
            self.create_send_internal('goto', position=(1.2, 1.53), angle=-0.8+math.pi)
        elif self.state == 'vers foyer du milieu' and msg.name == 'goto done':
            self.state = 'pose feu 3'
            if not self.robot.stopped:
                self.asserv.push_arm(1 + self.robot.color)
        elif self.state == 'pose feu 3' and msg.name == 'laid':
            self.state = 'après pose feu 3'
            self.create_send_internal('goto', position=(1.4, 1.25), angle=math.pi)
        elif self.state == 'après pose feu 3' and msg.name == 'goto done':
            self.state = 'avant pose feu 4'
            if not self.robot.stopped:
                self.asserv.raise_arm(2 - self.robot.color)
            self.create_send_internal('goto', position=(1.18, 1.06), angle=-2.36)
        elif self.state == 'avant pose feu 4' and msg.name == 'goto done':
            self.state = 'pose feu 4'
            if not self.robot.stopped:
                self.asserv.push_arm(2 - self.robot.color)
        elif self.state == 'pose feu 4' and msg.name == 'laid':
            self.state = 'filet'
            self.create_send_internal('filet')

