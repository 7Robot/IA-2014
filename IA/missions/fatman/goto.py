from missions.mission import Mission

class Goto(Mission):
    def __init__(self, robot, boardth):
        super().__init__(robot, boardth)
        self.name = 'Goto mission'
        self.position = None
        self.angle = None
        self.sick = False
        
    def go(self, msg):
        if msg.board == "internal" and msg.name == 'goto':
            self.position = msg.position
            self.angle = msg.angle
            if not self.sick:
                self.asserv.motion_pos(self.position[0], self.position[1])
            self.state = "going"            
        
        if msg.board == "asserv" and msg.name == 'sick':
            self.asserv.stop()
            self.sick = True

        if self.state == 'going' and msg.board == "asserv" and msg.name == 'done' and not self.sick:
            self.asserv.motion_angle(self.angle)
            self.state = 'turning'

        if self.state == 'turning' and msg.board == 'asserv' and msg.name == 'done' and not self.sick:
            self.state = "off"
            self.create_send_internal('goto done')
                
        if msg.board == 'asserv' and msg.name == 'freepath':
            self.sick = False
            if self.state == 'going':
                self.asserv.motion_pos(self.position[0], self.position[1])
            elif self.state == 'turning':
                self.asserv.motion_angle(self.angle)
