
from . import core

from types import ModuleType
from inspect import getmembers


# UTIL ------------------------------------------------------------------------

def validMembers(members):
    def validMembersGenerator(members):
        for key, val in members:
            if not key.startswith('_') and type(val) is not ModuleType:
                yield (key, val)
    return validMembersGenerator(members)


# PROCESSORS ------------------------------------------------------------------

def process_val(frame, key, val):
    core.globalize(frame, key, val)

def process_dict(frame, data):
    for key, val in data.items():
        core.globalize(frame, key, val)

def process_module(frame, module):
    members = module.__dict__.items()
    for (key, val) in validMembers(members):
        core.globalize(frame, key, val)

# class instance
def process_instance(frame, instance):
    members = getmembers(instance)
    for (key, val) in validMembers(members):
        core.globalize(frame, key, val)



# EXTENDED CLASS --------------------------------------------------------------

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

    # PROCESSORS --------------------------------------------------------------

    val         = core.frameDecorator(process_val)
    dict        = core.frameDecorator(process_dict)
    module      = core.frameDecorator(process_module)
    instance    = core.frameDecorator(process_instance)


    @core.frameDecorator
    def duck(frame, *args):
        try:
            return process_val(frame, *args)
        except:
            #print('val fail')
            pass
        try:
            return process_dict(frame, *args)
        except:
            #print('dict fail')
            pass
        try:
            return process_module(frame, *args)
        except:
            #print('module fail')
            pass
        #print('no assignment')



    @core.frameDecorator
    def type(frame, *args):
        if len(args) is 2:
            process_val(frame, *args)
        elif len(args) is 1:
            (data,) = args
            if isinstance(data, dict):
                process_dict(frame, data)
            elif isinstance(data, ModuleType):
                process_module(frame, data)
#            else:
#                process_instance(frame, data)
#                #try:
#                #    self.instance(data)
#                #except:
#                #    pass





