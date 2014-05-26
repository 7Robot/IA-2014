#/usr/bin/python

from missions.mission import Mission
import logging
from math import pi

class WaitForSignal(Mission):
    def __init__(self, robot, boardth):
        super(WaitForSignal, self).__init__(robot, boardth)
        self.name = 'Wait for start'

    def go(self, msg):
        if (self.state == 'off' and msg.board == 'asserv' and msg.name == 'start'):
            self.state = 'lances'
            self.create_timer(85.0, 'fin_du_match') #fin du match après 85sec (pour etre large)
            if msg.color == 0:
                Mission.data['color'] = 'rouge'
                self.asserv.setXYTheta(1.330, 0.475, pi)
            elif msg.color == 1:
                Mission.data['color'] = 'jaune'
                self.asserv.setXYTheta(-1.330, 0.475, pi)
            logging.warn('launcging lances order')
            self.create_send_internal('beginLances')

        elif (self.state =='lances' and msg.board == 'internal' and msg.name == 'endLances'):
            #self.create_send_internal('beginPeintures')
            state = 'off'


        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            logging.warn("End of match, stopping robot ...")
            self.asserv.stop()
            self.asserv.stopLaunch()
            self.state = 'off'
            
