import types
import inspect
import sys


if sys.version_info[0] < 3:
    def class_of(object):
        return object.im_class

else:
    def class_of(object):
        return object.__self__.__class__



def get_local_methods_of(object):
    results = {}
    for attr in dir(object):
        method = getattr(object, attr)
        if type(method) == types.MethodType and \
                        method.__name__ not in ('__init__') and \
                        method.__func__ in class_of(method).__dict__.values():
            args = inspect.getargspec(method)[0][1:]
            results[method.__name__] = args
    return results
