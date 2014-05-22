#/usr/bin/python

class Msg:
    def __init__(self, board, name, args=None, info=None):
        self.board = board.lower()
        self.name = name.lower()
        self.args = args
        if info is not None:
            self.info = info.lower()
        else:
            self.info = info

    def __getattr__(self, attr):
        return self.args[attr]

class InternalMsg(Msg):
    def __init__(self, name, args=None):
        super().__init__("internal", name, args)
