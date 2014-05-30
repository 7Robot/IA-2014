import logging
import math
from missions.mission import Mission

SICKS_FRONT = {2, 3}
SICKS_BACK = {0, 1}

class Goto(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.position = None
        self.last_position = None
        self.last_angle = None
        self.angle = None
        self.sicks = set()
        self.nosick = set()

    def move(self):
        if self.robot.stopped:
            return

        if len(self.position) == 1:
            self.asserv.motion_pos(self.position[0][0], self.position[0][1])
        else:
            self.asserv.motion_push(self.position[0][0], self.position[0][1], 0.1)
            self.asserv.motion_push(self.position[1][0], self.position[1][1], 0)
        self.state = "going"
    
    def go(self, msg):
        if self.robot.stopped:
            return

        if msg.name == 'reset goto':
            self.last_position = (0, 0)
            self.last_angle = math.pi
            self.asserv.setPos(0, 0, math.pi)

        elif msg.board == "internal" and msg.name == 'goto':
            if not isinstance(msg.position, list):
                msg.position = [msg.position]
            self.position = msg.position if self.robot.color == 1 else [(i[0], -i[1]) for i in msg.position]

            assert -math.pi <= msg.angle <= math.pi
            assert 0 < len(msg.position) < 3

            self.angle = msg.angle if self.robot.color == 1 else -msg.angle

            # calcul de la façon dont on va s'orienter pour trouver les sicks utiles
            angle = math.atan2(self.position[-1][1] - self.last_position[1], self.position[-1][0] - self.last_position[0])
            self.nosick = SICKS_BACK if abs(angle - self.last_angle) < math.pi / 2 else SICKS_FRONT
            try:
                self.nosick.update(msg.nosick)
            except:
                pass

            self.last_position = self.position[-1]
            self.last_angle = self.angle

            if self.sicks - self.nosick:
                self.state = "waiting"
            else:
                self.move()
        
        elif msg.board == "asserv" and msg.name == 'sick':
            self.sicks.add(msg.id)
            if self.state == 'going' and (self.sicks - self.nosick):
                self.asserv.block()
                self.state = "waiting"

        elif msg.board == 'turret' and msg.name == 'pos':
            if msg.distance > 6:
                if self.state == 'going':
                    self.asserv.block()
                    self.state = 'waiting'
            else:
                if self.state == 'waiting' and not(self.sicks - self.nosick):
                    self.move()

        elif self.state == 'going' and msg.board == "asserv" and msg.name == 'done':
            self.asserv.motion_angle(self.angle)
            self.state = 'turning'

        elif self.state == 'turning' and msg.board == 'asserv' and msg.name == 'done':
            self.state = "off"
            self.create_send_internal('goto done')
                
        elif msg.board == 'asserv' and msg.name == 'freepath':
            try:
                self.sicks.remove(msg.id)
            except KeyError:
                logging.warning("Freepath on an already free sick.")
            if not(self.sicks - self.nosick) and self.state == 'waiting':
                self.move()
