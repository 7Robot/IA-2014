from missions.mission import Mission

class SeqMission(Mission):
    
    actions = [
        #('nom', lambda self: self.create_send_internal('goto', position=(1,0), angle=), 'goto done'),
    ]

    def go(self, msg):
        try:
            n = [i for i, action in enumerate(self.actions) if action[0] == msg][0]
        except IndexError:
            n = -1

        if n == -1:
            self.state = self.actions[0][0]
            self.actions[0][1](self)
        elif msg.name == self.actions[n][2]:
            try:
                self.state = self.actions[n+1][0]
                self.actions[n+1][1](self)
            except IndexError:
                self.state = 'off'
