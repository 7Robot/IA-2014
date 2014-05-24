from missions.mission import Mission
import math

class Filet(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Filet mission'
        self.position = None
        self.angle = None
        
    def go(self, msg):
        if (msg.board == "internal" and msg.name == 'filet'):
            self.create_send_internal('goto', position=(0.6, 0.57), angle=math.pi)
            self.state = "going"
        
        elif (self.state == "going" and msg.board == 'internal' and msg.name == 'goto done'):
            self.asserv.launch_net()
            self.create_send_internal('filet done')
