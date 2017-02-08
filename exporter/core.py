

import sys
from inspect import getouterframes


def globalize(frame, key, val):
    frame.f_globals[key] = val


# FRAME INIT ------------------------------------------------------------------

class SetFrame:
    def __init__(self, frame_num):
        self.frame_num = frame_num
    def __enter__(self):
        frame_num = self.frame_num
        if frame_num >= 0:
            self.frame      = sys._getframe(frame_num)
        else:
            frame_current   = sys._getframe(0)
            frame_info      = getouterframes(frame_current)[frame_num]
            self.frame      = frame_info[0]
        return self.frame
    def __exit__(self, type, value, traceback):
        del self.frame


# DECORATOR -------------------------------------------------------------------

def frameDecorator(processor):
    def framer(self, *args):
        with SetFrame(self.frame_num) as frame:
            processor(frame, *args)
    return framer


# EXPORTER CLASS --------------------------------------------------------------

class Exporter:
    CURRENT = 2
    CALLING = 3
    TOP     = -1

    # PUBLIC ------------------------------------------------------------------

    def __init__(self, *frame_num):
        if frame_num:
            (self.frame_num,) = frame_num

    def setframe(self, frame_num):
        self.frame_num = frame_num
        return self
    def top(self):
        self.frame_num = self.TOP
        return self
    def current(self):
        self.frame_num = self.CURRENT
        return self
    def calling(self):
        self.frame_num = self.CALLING
        return self

    # PROCESSORS --------------------------------------------------------------

    val = frameDecorator(globalize)
    def val(frame, key, val):
        globalize(frame, key, val)




