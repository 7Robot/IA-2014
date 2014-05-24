from missions.mission import Mission

class Goto(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Goto mission'
        self.position = None
        self.angle = None
        
    def go(self, msg):
        if (msg.board == "internal" and msg.name == 'goto'):
            self.position = msg.position
            self.angle = msg.angle
            self.asserv.motion_pos(self.position[0], self.position[1])
            self.state = "going"            
        
        elif (self.state == "going"):
            if (msg.board == "internal" and msg.name == 'alert'):
                self.asserv.stop()
                self.state = "waiting"
            elif msg.board == "asserv" and msg.name == 'done':
                self.asserv.motion_angle(self.angle)
                self.state = 'turning'

        elif self.state == 'turning':
            if msg.board == 'asserv' and msg.name == 'done':
                self.state = "off"
                self.create_send_internal('goto done')
                
        elif (self.state == "waiting"):
            if (msg.board == 'asserv' and msg.name == 'freepath'):
                self.walk(self.axe, self.target)
                self.state = "forward"
                
