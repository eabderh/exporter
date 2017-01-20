
from types import ModuleType
from .core import globalize


def validMembers(members):
    def validMembersGenerator(members):
        for key, val in members:
            if not key.startswith('_') and type(val) is not ModuleType:
                yield (key, val)
    return validMembersGenerator(members)
#    for key, val in members:
#        if not key.startswith('_') and type(val) is not ModuleType:
#            globalize(frame, key, val)


# PROCESSORS ------------------------------------------------------------------

def dict(frame, data):
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


