
from typing import Literal

def _recursive_rewrite_literals(params):
    if hasattr(params, '__iter__'):
        orig_type = type(params)
        params = list(params)
        for i, param in enumerate(params):
            params[i] = _recursive_rewrite_literals(param)
        params = orig_type(params)
    elif isinstance(params, int):
        params = Literal[params] # type: ignore

    return params

class IntTypeArgs:
    def __class_getitem__(self, params):
        params = _recursive_rewrite_literals(params)
        return super().__class_getitem__(params)