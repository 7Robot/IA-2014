from missions.mission import Mission
import logging

class Forward(Mission):
    def __init__(self, robot, boardth):
        super(Forward, self).__init__(robot, boardth)
        self.name = 'Forward mission'
        self.target = None
        self.axe = None
        
    def walk(axe, target):
        if (axe == 'x'):
            self.asserv.reachX(target, 0.1, 0.1)
        elif (axe == 'y'):
            self.asserv.reachY(target, 0.1, 0.1)
        
    def go(self, msg):
        if (msg.board == "internal" and msg.name == 'forward'):
            self.target = msg.target
            self.axe = msg.axe  
            self.current_mission = msg.mission
            self.walk(msg.axe, msg.target)
            self.state = "forward"            
        
        elif (self.state == "forward"):
            if (msg.board == "internal" and msg.name == 'alert'):
                self.asserv.stop()
                self.state = "waiting"
            elif msg.board == "asserv" and msg.name == 'done'):
                self.target = None
                self.axe = None
                self.state = "off"
                self.create_send_internal('done')
                self.current_mission = None
                
        elif (self.state == "waiting"):
            if (msg.board == 'asserv' and msg.name == 'freepath'):
                self.walk(self.axe, self.target)
                self.state = "forward"
                
