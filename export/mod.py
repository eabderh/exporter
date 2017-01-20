

from . import common as cm


def val(key, val):
    with cm.callingFrame() as frame:
        cm.processVal(frame, key, val)

def dict(data):
    with cm.callingFrame() as frame:
        cm.processDict(frame, data)

def instance(instance):
    with cm.callingFrame() as frame:
        cm.processInstance(frame, instance)

def module(module):
    with cm.callingFrame() as frame:
        cm.processModule(frame, module)



