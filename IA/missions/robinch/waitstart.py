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
            self.asserv.setBalls(6)
            if msg.color == 0:
                Mission.data['color'] = 'rouge'
                self.asserv.setXYTheta(1.330, 0.482, pi)
                self.create_send_internal('backsick') 
            elif msg.color == 1:
                Mission.data['color'] = 'jaune'
                self.asserv.setXYTheta(-1.330, 0.482, pi)
                self.create_send_internal('frontsick') 
            #self.create_send_internal('beginHomolog')
            self.create_send_internal('beginLances')
            
        elif (self.state =='lances' and msg.board == 'internal' and msg.name == 'endHomolog'):
            self.create_send_internal('fin_du_match')

        elif (self.state =='lances' and msg.board == 'internal' and msg.name == 'endLances'):
            self.create_send_internal('beginBaroud')
            self.state = 'baroud'

        elif (self.state =='baroud' and msg.board == 'internal' and msg.name == 'endBaroud'):
            self.create_send_internal('beginPeintures')
            self.state = 'fin'
            
        elif (self.state =='fin' and msg.board == 'internal' and msg.name == 'endPeintures'):
            self.create_send_internal('fin_du_match')

        elif (msg.board == "internal" and msg.name == "fin_du_match"):
            logging.warn("End of match, stopping robot ...")
            self.asserv.stop()
            self.asserv.stopLaunch()
            self.state = 'off'
            
