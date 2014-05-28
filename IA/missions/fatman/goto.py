import logging
from missions.mission import Mission

class Goto(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.position = None
        self.angle = None
        self.sicks = set()
        
    def go(self, msg):
        if msg.board == "internal" and msg.name == 'goto':
            self.position = msg.position if self.robot.color == 1 else (msg.position[0], -msg.position[1])
            self.angle = msg.angle if self.robot.color == 1 else -msg.angle
            self.asserv.motion_pos(self.position[0], self.position[1])
            try:
                self.nosick = set(msg.nosick)
            except:
                self.nosick = set()
            self.state = "going"
        
        elif msg.board == "asserv" and msg.name == 'sick':
            self.sicks.add(msg.id)
            if self.state == 'going' and self.sicks > self.nosick:
                self.asserv.block()
                self.state = "waiting"

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
            if not self.sicks and self.state == 'waiting':
                self.asserv.motion_pos(self.position[0], self.position[1])
                self.state = "going"
                
