

def validMembers(members):
    def validMembersGenerator(members):
        for key, val in members:
            if not key.startswith('_') and type(val) is not ModuleType:
                yield (key, val)
    return validMembersGenerator(members)


def dict(frame, dictionary):
    frame.f_globals.update(dictionary)

def val(frame, key, val):
    frame.f_globals[key] = val

def module(frame, module):
    members = module.__dict__.items()
    for (key, val) in validMembers(members):
        core.globalize(frame, key, val)

# class instance
def instance(frame, instance):
    members = getmembers(instance)
    for (key, val) in validMembers(members):
        core.globalize(frame, key, val)


