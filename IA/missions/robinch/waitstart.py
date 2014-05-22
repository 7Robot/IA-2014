#/usr/bin/python

from missions.mission import Mission
import logging

class WaitForSignal(Mission):
    def __init__(self, robot, boardth):
        super(WaitForSignal, self).__init__(robot, boardth)
        self.name = 'Wait for start'

    def go(self, msg):
        if (self.state == 'off' and msg.board == 'asserv' and msg.name == 'start'):
            logging.warn("starting mission %s" % self.name)
            self.create_timer(85.0, 'fin_du_match'): #fin du match après 85sec (pour etre large)
            if msg.color == 0:
                Mission.data['color'] = 'rouge'
            elif msg.color == 1:
                Mission.data['color'] = 'jaune'

            self.create_send_internal('beginmatch')

        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            logging.warn("End of match, stopping robot ...")
            self.asserv.stop()
            self.state = 'off'
            
