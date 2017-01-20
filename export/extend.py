
from . import core
from .core import frameDecorator
from .core import globalize
from .util import validMembers
from . import util

from types import ModuleType
from inspect import getmembers




# PROCESSORS ------------------------------------------------------------------
def val(frame, key, val):
    globalize(frame, key, val)

def _dict(frame, data):
    for key, val in data.items():
        globalize(frame, key, val)

def module(frame, module):
    members = module.__dict__.items()
    for (key, val) in validMembers(members):
        globalize(frame, key, val)

# class instance
def instance(frame, instance):
    members = getmembers(instance)
    for (key, val) in validMembers(members):
        globalize(frame, key, val)





class Exporter(core.Exporter):

    # PUBLIC ------------------------------------------------------------------
    def top(self):
        self.frame_num = Exporter.TOP
        return self
    def current(self):
        self.frame_num = Exporter.CURRENT
        return self
    def calling(self):
        self.frame_num = Exporter.CALLING
        return self


    @frameDecorator
    def duck(frame, *args):
        try:
            return val(frame, *args)
        except:
            print('val fail')
            pass
        try:
            return _dict(frame, *args)
        except:
            print('dict fail')
            pass
        try:
            return module(frame, *args)
        except:
            print('module fail')
            pass
        print('no assignment')



#    @frameDecorator
#    def duck(frame, *args):
#        if len(args) is 2:
#            val(frame, *args)
#        elif len(args) is 1:
#            (data,) = args
#            if isinstance(data, dict):
#                _dict(frame, data)
#            elif isinstance(data, ModuleType):
#                module(frame, data)
#            else:
#                instance(frame, data)
#                #try:
#                #    self.instance(data)
#                #except:
#                #    pass

    # PROCESSORS --------------------------------------------------------------

    dict = frameDecorator(_dict)
    module = frameDecorator(module)
    instance = frameDecorator(instance)




