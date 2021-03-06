from missions.mission import Mission
import math

class Filet(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.position = None
        self.angle = None
        
    def go(self, msg):
        if msg.board == "internal" and msg.name == 'filet' and self.state == 'off':
            self.create_send_internal('goto', position=(0.51, 0.86), angle=-math.pi)
            self.state = "going"
        
        elif self.state == "going" and msg.name == 'goto done':
            self.state = 'waiting'

        elif msg.name == 'funny action' and self.state == 'waiting':
            self.asserv.launch_net()
