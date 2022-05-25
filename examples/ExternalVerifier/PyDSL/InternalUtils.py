"""
This file contains internal helper functions that are not intended for the use outside of PyDSL.
"""


def get_fqcn(cn: object):
    """
    Get fully qualified class name
    """
    fqcn = cn.__module__
    if hasattr(cn, '__qualname__'):
        fqcn += f".{cn.__qualname__}"  # type:ignore

    return fqcn
