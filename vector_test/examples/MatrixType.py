# import logging

# from math import prod
# from typing import Generic, TypeVar, Literal, Tuple

# T = TypeVar("T")
# U = TypeVar("U")
# V = TypeVar("V")

# def _recursive_rewrite_literals(params):
#     if hasattr(params, '__iter__'):
#         orig_type = type(params)
#         params = list(params)
#         for i, param in enumerate(params):
#             params[i] = _recursive_rewrite_literals(param)
#         params = orig_type(params)
#     elif isinstance(params, int):
#         params = Literal[params] # type: ignore

#     return params

# class Vector(Generic[T, U, V]):
#     def __init__(self, l):
#         self.dims = (2, 3)
#         self.l = l

#     def __class_getitem__(self, params):
#         params = _recursive_rewrite_literals(params)
#         return super().__class_getitem__(params)

#     def __add__(self, other : 'Vector[int, 2, 3]') -> 'Vector[int, 2, 3]':
#        if self.get_dims() != other.get_dims():
#            logging.error("Added vectors must have the same dimensions.\n"
#                          f"{self.get_dims()} != {other.get_dims()}")

#        p = prod(self.dims)
#        r = []
#        for i in range(p):
#            r.append(self.l[i] + other.l[i])

#        z : Vector[int, 2, 3] = Vector(r)
#        return z

#     def __str__(self):
#        return f"Vector({'x'.join(map(str, self.dims))}) = [{', '.join(map(str, self.l))}]"

#     def get_dims(self) -> Tuple[int, int]:
#        return self.dims

