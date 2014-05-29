from missions.mission import Mission
import logging
from time import sleep


def inverser(fonction):
    def fonction2(self, axe, target):
        if Mission.data['color'] == 'rouge' and axe =='x':
            target = -target
        fonction(self, axe, target)
    return fonction2
    

class Forward(Mission):
    def __init__(self, robot, boardth):
        super(Forward, self).__init__(robot, boardth)
        self.name = 'Forward mission'
        self.target = None
        self.axe = None
        
    @inverser
    def walk(self, axe, target):
        if (axe == 'x'):
            self.asserv.reachX(target, 0.1, 0.05)
        elif (axe == 'y'):
            self.asserv.reachY(target, 0.1, 0.05)
        
    def go(self, msg):
        if (msg.board == "internal" and msg.name == 'forward'):
            self.target = msg.target
            self.axe = msg.axe  
            self.walk(msg.axe, msg.target)
            self.state = "forward"            
        
        elif (self.state == "forward"):
            if (msg.board == "internal" and msg.name == 'alert'):
                self.asserv.block()
                self.state = "waiting"
            elif (msg.board == "asserv" and msg.name == 'done'):
                self.target = None
                self.axe = None
                self.state = "off"
                self.create_send_internal('forward_done')
                
        elif (self.state == "waiting"):
            if (msg.board == 'internal' and msg.name == 'freepath'):
                self.walk(self.axe, self.target)
                self.state = "forward"
            elif (msg.board == "asserv" and msg.name == 'done'):
                self.target = None
                self.axe = None
                self.state = "off"
                self.create_send_internal('forward_done')

        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            self.state = 'off'

