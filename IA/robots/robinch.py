#/usr/bin/python3

from mathutils.types import Vertex
from queue import Queue


class Robinch:
    def __init__(self):
        self.name = 'robinch'
        self.transmitter = 'arm'
        self.boards  = { "Asserv": 1301, "Turret": 1308 }
        self.semantic = '../semantic_robinch.py'
        self.host = 'localhost'
        self.queue = Queue()

        #position et orientation initiale du robot
        self.pos = Vertex(-12000, -7000)
        self.rot = 0

        self.sensor_front = None 
        self.sensor_back = None
