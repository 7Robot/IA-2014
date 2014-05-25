from missions.mission import Mission
import math

class Convoyer(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Convoyer mission'
        
    def go(self, msg):
        if (msg.board == "internal" and msg.name == 'convoyer'):
            self.create_send_internal('goto', position=(0.3, 0.6), angle=math.pi)
            self.state = "going"            
        
        elif self.state == "going" and msg.name == 'goto done':
            self.asserv.convoyer()
            self.state = "convoyage"

        elif self.state == 'convoyage' and msg.board == 'asserv' and msg.name == 'done':
            self.create_send_internal('convoyer done')
            self.state = 'off'
