#!/usr/bin/python

from missions.mission import Mission
import math

SICKS = (0,1,2,3)

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
            self.create_timer(1, 'timer start')
            self.create_timer(92, 'funny action')
            self.create_timer(87, 'stop')
            self.create_timer(80, 'filet')
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
            self.create_send_internal('goto', position=[(0.6, 0.22), (0.79, 0.22)], angle=math.pi/2)
        elif self.state == 'devant deuxième feu' and msg.name == 'goto done':
            self.state = 'prendre deuxième feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(2 - self.robot.color)
        elif self.state == 'prendre deuxième feu' and msg.name == 'caught':
        # POSE DES FEUX
            self.state = 'pose feux'
            if not self.robot.stopped:
                self.asserv.raise_arm(2 - self.robot.color)
            self.create_send_internal('goto', position=(1.65, 0.16), angle=0.8)
        elif self.state == 'pose feux' and msg.name == 'goto done':
            self.state = 'pose feu 1'
            if not self.robot.stopped:
                self.asserv.push_arm(2 - self.robot.color)
        elif self.state == 'pose feu 1' and msg.name == 'laid':
            self.state = 'demi tour feu 2'
            if not self.robot.stopped:
                self.asserv.raise_arm(1 + self.robot.color)
            self.create_send_internal('goto', position=(1.54, 0.06), angle=0.8-math.pi)
        elif self.state == 'demi tour feu 2' and msg.name == 'goto done':
            if not self.robot.stopped:
                self.asserv.pull_arm(1 + self.robot.color)
            self.state = 'pose feu 2'
        elif self.state == 'pose feu 2' and msg.name == 'laid':
        # FIN POSE FEUX
            self.state = 'devant troisième feu'
            self.create_send_internal('goto', position=(1.5, 0.52), angle=math.pi, nosick=SICKS)
        elif self.state == 'devant troisième feu' and msg.name == 'goto done':
            self.state = 'prendre troisième feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(2 - self.robot.color)
        elif self.state == 'prendre troisième feu' and msg.name == 'caught':
            self.state = 'devant quatrième feu'
            self.create_send_internal('goto', position=(1.68, 1.135), angle=-math.pi/2, nosick=SICKS)
        elif self.state == 'devant quatrième feu' and msg.name == 'goto done':
            self.state = 'prendre quatrième feu'
            if not self.robot.stopped:
                self.asserv.catch_arm(1 + self.robot.color)
        elif self.state == 'prendre quatrième feu' and msg.name == 'caught':
        # FOYER MILIEU
            self.state = 'vers foyer du milieu'
            if not self.robot.stopped:
                self.asserv.raise_arm(2 - self.robot.color)
            self.create_send_internal('goto', position=(1.3, 1.38), angle=-math.pi/2)
        elif self.state == 'vers foyer du milieu' and msg.name == 'goto done':
            self.state = 'pose feu 3'
            if not self.robot.stopped:
                self.asserv.pull_arm(2 - self.robot.color)
        elif self.state == 'pose feu 3' and msg.name == 'laid':
            self.state = 'avant pose feu 4'
            if not self.robot.stopped:
                self.asserv.raise_arm(1 + self.robot.color)
            self.create_send_internal('goto', position=[(1.4, 1), (1.04, 1.00)], angle=0.3)
        elif self.state == 'avant pose feu 4' and msg.name == 'goto done':
            self.state = 'pose feu 4'
            if not self.robot.stopped:
                self.asserv.push_arm(1 + self.robot.color)
        elif self.state == 'pose feu 4' and msg.name == 'laid':
            self.state = 'filet'
            self.create_send_internal('filet')
        elif msg.board == 'internal' and msg.name == 'filet':
            self.state = 'filet'

