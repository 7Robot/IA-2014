#/usr/bin/python

import threading
import socket
from atp.channel import Channel
from atp.protos import load as load_protos
import logging
from msg.msg import Msg

class BoardThread(threading.Thread):
    def __init__(self, robot):
        super().__init__()

        self.robot = robot
        self.channels = dict()
        self.streams = dict()
        self.host = self.robot.host
        self.logging = logging

        protos = load_protos(self.robot.semantic)
        for board in self.robot.boards:
            sock = socket.socket()
            port = self.robot.boards[board]
            sock.connect((self.host, port))
            file = sock.makefile(mode="rw")
            stream = file.buffer
            proto = protos[board]
            channel = Channel(stream, lambda name, args, board = board: self.callback(board, name, args), board, proto, transmitter = self.robot.transmitter)
            self.channels[board] = channel
            self.streams[board] = (sock, file, stream)


    def callback(self, board, name, args):
        self.logging.warn("[%s.%s]" %(board, name))
        for arg in args:
            self.logging.warn("\t%s:%s" % (arg, args[arg]))
        msg = Msg(board, name, args)
        self.robot.queue.put(msg, True)
