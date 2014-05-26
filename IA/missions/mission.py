#/usr/bin/python
import logging
from msg.msg import Msg, InternalMsg
import threading

class Mission:

    data = {}

    def __init__(self, robot, boardth):
        self.robot = robot
        self._state = 'off'
        
        boards = boardth.channels
        for b in boards:
            setattr(self,b.lower(),boards[b])

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        logging.warn("[%s:state] %s -> %s" %(self.__class__.__name__, self.state, state))
        self._state = state
    
    state = property(_get_state, _set_state)

    def create_send_event(self, board, name, **kwargs):
        m = Msg(board, name, kwargs)
        self.robot.queue.put(m, True)

    def create_send_internal(self, name, **kwargs):
        m = InternalMsg(name, kwargs)
        self.robot.queue.put(m, True)
        
    def send_event(self, msg):
        self.robot.queue.put(msg, True)
        
    def create_timer(self, duration, timername=None):
        '''Creer un timer qui va envoyer un evenement interne Timer_end. 
        self.create_send_internal se termine immediatement apres l'ajout dans la queue
        donc le thread du Timer s'arrete apres l'execution du send_internal()
        donc il n'y a pas de probleme d'execution concurrente entre le thread du timer
        et l'ia qui gere les missions'''
        t = threading.Timer(duration, self.create_send_internal, [timername])
        t.start()

    def go(self, msg):
        raise NotImplementedError()
