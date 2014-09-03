#!/usr/bin/python

import argparse, configparser
import sys
import socket

from atp.protos import load as load_protos
from atp.channel import Channel, print_packet

import robots
import ia
import boardThread

if __name__ == "__main__":
    try:
        robot_name = sys.argv[1]
    except IndexError:
        print("Usage : main.py RobotName")
        exit()
    robot = getattr(robots, robot_name)()
    boardth = boardThread.BoardThread(robot)
    boardth.start()
    IA = ia.IA(robot, boardth)
    IA.run()


#pouet