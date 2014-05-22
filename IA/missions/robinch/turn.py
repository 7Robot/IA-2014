from missions.mission import Mission
import logging

class Turn(Mission):
    def __init__(self, robot, boardth):
        super(Turn, self).__init__(robot, boardth)
        self.name = 'Turning mission'
        
    def go(self, msg):
        if (msg.board == "internal" and msg.name == 'turn'):
            self.asserv.reachTheta(msg.target, 0.1, 0.1)
            self.state = "turning"

        elif (self.state == "turning"):
            if msg.board == "asserv" and msg.name == 'done'):
                self.target = None
                self.axe = None
                self.state = "off"
