
import sys
from types import ModuleType
from inspect import currentframe
from inspect import getouterframes
from inspect import getmembers


def globalize(frame, key, val):
    frame.f_globals[key] = val


class topFrame:
    def __enter__(self):
#        thisframe = currentframe()
        thisframe = sys._getframe(0)
        topframeinfo = getouterframes(thisframe)[-1]
        self.topframe = topframeinfo[0]
        return self.topframe
    def __exit__(self, type, value, traceback):
        del self.topframe

class callingFrame:
    def __enter__(self):
#        thisframe = currentframe()
#        # go back twice since this function generated a new calling frame
#        self.callingframe = thisframe.f_back.f_back
        self.callingframe = sys._getframe(2)
        return self.callingframe
    def __exit__(self, type, value, traceback):
        del self.callingframe


def processVal(frame, key, val):
    globalize(frame, key, val)

def processDict(frame, data):
    for key, val in data.items():
        globalize(frame, key, val)

def processInstance(frame, instance):
    members = getmembers(instance)
    for key, val in members:
        if not key.startswith('_') and type(val) is not ModuleType:
            globalize(frame, key, val)

def processModule(frame, module):
    members = module.__dict__.items()
    for key, val in members:
        if not key.startswith('_') and type(val) is not ModuleType:
            globalize(frame, key, val)



