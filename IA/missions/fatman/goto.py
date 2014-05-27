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
                self.nosick = msg.nosick
            except:
                self.nosick = set()
            self.state = "going"
        
        elif self.state == "going":
            if msg.board == "asserv" and msg.name == 'sick' and msg.id not in self.nosick:
                self.sicks.add(msg.id)
                self.asserv.block()
                self.state = "waiting"
            elif msg.board == "asserv" and msg.name == 'done':
                self.asserv.motion_angle(self.angle)
                self.state = 'turning'

        elif self.state == 'turning':
            if msg.board == 'asserv' and msg.name == 'done':
                self.state = "off"
                self.create_send_internal('goto done')
                
        elif self.state == "waiting":
            if msg.board == 'asserv' and msg.name == 'freepath':
                self.sicks.remove(msg.id)
                if not self.sicks:
                    self.asserv.motion_pos(self.position[0], self.position[1])
                    self.state = "going"
                
