

import sys
import inspect
import types

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
            frame_info      = inspect.getouterframes(frame_current)[frame_num]
            self.frame      = frame_info[0]
        return self.frame
    def __exit__(self, type, value, traceback):
        del self.frame


# DECORATOR -------------------------------------------------------------------

def frameDecorator(processor):
    def _framed_processor(self, *args):
        with SetFrame(self.frame_num) as frame:
            processor(frame, *args)
    return _framed_processor

# PROCESSORS ------------------------------------------------------------------

def process_val(frame, key, val):
    frame.f_globals[key] = val

def process_dict(frame, dictionary):
    frame.f_globals.update(dictionary)

def process_module(frame, module):
    for (key, val) in module.__dict__.items():
        if isValidPair(key, val):
            frame.f_globals[key] = val

def isValidPair(key, val):
    return not key.startswith('__') and type(val) is not types.ModuleType



# EXPORTER CLASS --------------------------------------------------------------

class Export:
    CURRENT = 2
    CALLING = 3
    TOP     = -1

    # PUBLIC ------------------------------------------------------------------

    def __init__(self, *frame_num):
        self.frame_num = self.TOP
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


    # PUBLIC METHODS ----------------------------------------------------------

    @frameDecorator
    def val(*args):
        process_val(*args)

    @frameDecorator
    def dict(*args):
        process_dict(*args)

    @frameDecorator
    def module(*args):
        process_module(*args)

    @frameDecorator
    def duck(frame, *args):
        try:
            return process_val(frame, *args)
        except:
            pass
        try:
            return process_dict(frame, *args)
        except:
            pass
        try:
            return process_module(frame, *args)
        except:
            pass

    @frameDecorator
    def type(frame, *args):
        if len(args) is 2:
            process_val(frame, *args)
        elif len(args) is 1:
            (data,) = args
            if isinstance(data, dict):
                process_dict(frame, data)
            elif isinstance(data, types.ModuleType):
                process_module(frame, data)








