
from typing import Callable, Dict

class _Constraints(object):
    """
    Internal structure storing all registered constraints.
    Register a new constraint with the decorator @constraint.
    """

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.constraints : Dict[str, Callable] = dict()
            cls.instance = super(_Constraints, cls).__new__(cls)
        return cls.instance

    def __iter__(self):
        return self.constraints.__iter__()

    def __next__(self):
        return self.constraints.__next__()

    def add(cls, k : str, c : Callable):
        cls.constraints[k] = c

def _get_fqcn(o : object):
    """
    Get fully qualified class name
    """
    cn = o.__class__
    return f"{cn.__module__}.{cn.__qualname__}"

def constraint(class_name):
    """
    Decorator to add callable constraint.
    """
    def decorate(fn):
        print("register vector")
        fqcn = _get_fqcn(class_name)
        _Constraints().add(fqcn, fn)
        return fn
    return decorate
