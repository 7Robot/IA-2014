#/usr/bin/python3

from mathutils.types import Vertex
from queue import Queue

class Fatman:
    def __init__(self):
        self.name = 'fatman'
        self.transmitter = 'arm'
        self.boards  = { "Asserv": 1302}
        self.semantic = '../semantic_fatman.py'
        self.host = 'localhost'
        self.queue = Queue()

        #position et orientation initiale du robot
        self.pos = Vertex(-12000, -7000)
        self.rot = 0

        self.sensor_front = None 
        self.sensor_back = None
