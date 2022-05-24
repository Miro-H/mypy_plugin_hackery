
from cmath import atan
from .Const import *
from typing import Callable, Dict, List, Union, Tuple
from mypy.types import (
    AnyType, Type, TypeOfAny, RawExpressionType, LiteralType
)
from mypy.plugin import AnalyzeTypeContext

class Constraints(object):
    """
    Internal structure storing all registered constraints.
    Register a new constraint with the decorator @constraint.
    """

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._constraints : Dict[str, Callable] = dict()
            cls.instance = super(Constraints, cls).__new__(cls)
        return cls.instance

    def __setitem__(self, key : str, item : Callable):
        self._constraints[key] = item

    def __getitem__(self, key : str) -> Callable:
        return self._constraints[key]

    def __repr__(self) -> str:
        return repr(self._constraints)

    def __len__(self) -> int:
        return len(self._constraints)
    
    def items(self):
        return self._constraints.items()

    def keys(self):
        return self._constraints.keys()

    def values(self):
        return self._constraints.values()

def _get_fqcn(o : object):
    """
    Get fully qualified class name
    """
    cn = o
    fqcn = cn.__module__
    if hasattr(cn, '__qualname__'):
        fqcn += f".{cn.__qualname__}" # type:ignore
    
    return fqcn

# def heco_vector_analyze_callback(ctx: AnalyzeTypeContext) -> Type:
    # args = ctx.type.args
    # t0 = ctx.api.analyze_type(args[0])
    # t_ts : List[Type] = [t0]

    # if len(args) == 2:
    #     success = True
    #     if _is_builtins_int(t0) and _is_literal_int(args[1]):
    #         # Accept definitions of the form Vector[int, nr], where nr is a literal int
    #         t_ts = [ 
    #             t0,
    #             LiteralType(value=args[1].literal_value, # type: ignore
    #                 fallback=ctx.api.named_type(args[1].base_type_name, [])) # type: ignore
    #         ]
    #     elif isinstance(t0, TypeVarType):
    #         # Accept definitions in class with unspecified type variables (e.g., Vector[T, U]) 
    #         t1 = ctx.api.analyze_type(args[1])
    #         if isinstance(t0, TypeVarType):
    #             t_ts = [t0, t1]
    #     else: 
    #         success = False
        
    #     if success:
    #         r = ctx.api.named_type(VECTOR_TYPE_NAME, t_ts)
    #         # print("Return r =", r)
    #         return r

    # ctx.api.fail('Invalid "Vector" type (expected "Vector[int, nr]")', ctx.context)
    # return AnyType(TypeOfAny.from_error)

class ConstraintContext:
    """
    This class holds context that is useful to evaluate if a typed instance
    of a custom class is valid or not.

    Attributes:
        standard : List[bool];  list defining whether the type at the same 
                                position in `types` was generated following
                                standard MyPy convention or not.
        
        types : List[Type];     MyPy types of the type arguments of the 
                                instance, e.g., for `Vector[int, 6]` this is
                                `builtins.int, Literal[6]`
    """

    def __init__(self, at_ctx: AnalyzeTypeContext) -> None:
        self.at_ctx = at_ctx

        # Analyze types of arguments and convert builtin.{int,bool} literals `a` 
        # to `Literal[a]`.
        self.types = []
        self.standard = []
        for arg in at_ctx.type.args:
            t_parsed, was_custom_parsed = self.parse_type(arg)
            self.standard.append(was_custom_parsed)
            self.types.append(t_parsed)

    def parse_type(self, t : Type) -> Tuple[Type, bool]:
        if (isinstance(t, RawExpressionType) 
                and t.base_type_name in [_get_fqcn(int), _get_fqcn(bool)]):

            t_parsed = LiteralType(
                value=t.literal_value, # type: ignore
                fallback=self.at_ctx.api.named_type(t.base_type_name, [])
            )
            return t_parsed, True
            
        return self.at_ctx.api.analyze_type(t), False


def constraint(class_name):
    """
    Decorator to add callable constraint to Constraints and process the
    AnalyzeTypeContext from mypy.plugin to a simpler ConstraintContext
    object.
    """
    def decorate(fn : Callable[[ConstraintContext], Union[bool, Tuple[bool, str]]]):
        fqcn = _get_fqcn(class_name)

        def mypy_callback_wrapper(at_ctx: AnalyzeTypeContext) -> Type:
            constraint_ctx = ConstraintContext(at_ctx)
            
            success = fn(constraint_ctx)
            err = DEFAULT_CONSTRAINT_FAILED_ERROR_MSG.format(fqcn)

            if isinstance(success, tuple):
                success, err = success

            if success:
                return at_ctx.api.named_type(fqcn, constraint_ctx.types)
            else:
                at_ctx.api.fail(err, at_ctx.context)
                return AnyType(TypeOfAny.from_error)

        Constraints()[fqcn] = mypy_callback_wrapper

        return mypy_callback_wrapper
    
    return decorate
