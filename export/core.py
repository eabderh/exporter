

import sys
from inspect import getouterframes


def globalize(frame, key, val):
    frame.f_globals[key] = val


class Frame:
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





class Exporter:
    CURRENT = 0
    CALLING = 2
    TOP     = -1

    # PUBLIC ------------------------------------------------------------------

    def __init__(self, frame_num):
        self.frame_num = frame_num
    def frame(self, frame_num):
        self.frame_num = frame_num
    def duck(self, *args):
        if len(args) is 2:
            self.val(*args)
        elif len(args) is 1:
            data = args[0]
            if isinstance(data, dict):
                self.dict(data)
            elif isinstance(data, ModuleType):
                self.module(data)
            else:
                self.instance(data)
                #try:
                #    self.instance(data)
                #except:
                #    pass



    # DECORATOR ---------------------------------------------------------------

    # wrap every decorating target (processors) with the framer function
    def frameDecorator(processor):
        def framer(self, *args):
            with Frame(self.frame_num) as frame:
                processor(frame, *args)
        return framer

    # PROCESSORS --------------------------------------------------------------

    @frameDecorator
    def val(frame, key, val):
        globalize(frame, key, val)

    @frameDecorator
    def dict(frame, data):
        for key, val in data.items():
            globalize(frame, key, val)

    @frameDecorator
    def module(frame, module):
        members = module.__dict__.items()
        for (key, val) in validMembers(members):
            globalize(frame, key, val)

    # class instance
    @frameDecorator
    def instance(frame, instance):
        members = getmembers(instance)
        for (key, val) in validMembers(members):
            globalize(frame, key, val)

    # PRIVATE -----------------------------------------------------------------

    @staticmethod
    def validMembers(members):
        def validMembersGenerator(members):
            for key, val in members:
                if not key.startswith('_') and type(val) is not ModuleType:
                    yield (key, val)
        return validMembersGenerator(members)
    #    for key, val in members:
    #        if not key.startswith('_') and type(val) is not ModuleType:
    #            globalize(frame, key, val)


extop = Exporter(Exporter.TOP)

export = Exporter(Exporter.TOP)

export.val('export', export)




