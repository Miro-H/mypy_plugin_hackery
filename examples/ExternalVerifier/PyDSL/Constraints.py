import builtins
import logging

from PyDSL.CustomTypes import IntTypeArgs, BoolTypeArgs
from .Const import *
from typing import Callable, Dict, List, Union, Tuple, TypeVar
from mypy.types import (
    AnyType, Instance, LiteralType, RawExpressionType,
    Type, TypeOfAny, TypeVarType
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
            cls._constraints: Dict[str, Callable] = dict()
            cls.instance = super(Constraints, cls).__new__(cls)
        return cls.instance

    def __setitem__(self, key: str, item: Callable):
        if key in self._constraints:
            logging.warning(CONSTRAINTS_OVERWRITING_WARNING.format(key))
        self._constraints[key] = item

    def __getitem__(self, key: str) -> Callable:
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


def _get_fqcn(o: object):
    """
    Get fully qualified class name
    """
    cn = o
    fqcn = cn.__module__
    if hasattr(cn, '__qualname__'):
        fqcn += f".{cn.__qualname__}"  # type:ignore

    return fqcn


class ConstraintContext:
    """
    This class holds context that is useful to evaluate if a typed instance
    of a custom class is valid or not.

    Attributes:
        standard : List[bool];  list defining whether the type at the same 
                                position in `types` was generated following
                                standard MyPy convention or not.

        types : List[Type]; MyPy types of the type arguments of the
                            instance, e.g., for `Vector[int, 6]` this is
                            `builtins.int, Literal[6]`

        types_raw : List[object];   Reconstructed raw types of the type hints,
                                    e.g., for `Vector[int, 6]` this is [int, 6]

        at_ctx : AnalyzeTypeContext;    The full context provided by MyPy to
                                        the type analyzing hooks.
    """

    def __init__(self, at_ctx: AnalyzeTypeContext, obj) -> None:
        self.at_ctx = at_ctx

        # If the class inherits from IntTypeArgs and/or BoolTypeArgs, activate
        # custom literal parsing.
        mro = obj.mro()
        self.allow_raw_int_types = IntTypeArgs in obj.mro()
        self.allow_raw_bool_types = BoolTypeArgs in obj.mro()

        # Analyze types of arguments and convert builtin.{int,bool} literals `a`
        # to `Literal[a]` is custom literal parsing is active.
        self.types = []
        self.types_raw = []
        self.standard = []
        for arg in at_ctx.type.args:
            t_parsed, t_raw, was_custom_parsed = self.parse_type(arg)
            self.types.append(t_parsed)
            self.types_raw.append(t_raw)
            self.standard.append(was_custom_parsed)

    def parse_type(self, t: Type) -> Tuple[Type, object, bool]:
        if isinstance(t, RawExpressionType):
            do_parse_raw_int = (self.allow_raw_int_types
                                and t.base_type_name == _get_fqcn(int))
            do_parse_raw_bool = (self.allow_raw_bool_types
                                 and t.base_type_name == _get_fqcn(bool))

            if do_parse_raw_int or do_parse_raw_bool:
                t_raw = t.literal_value
                t_lit = LiteralType(
                    value=t_raw,  # type: ignore
                    fallback=self.at_ctx.api.named_type(t.base_type_name, [])
                )
                return t_lit, t_raw, True

            err = PARSE_TYPE_UNEXPECTED_RAW.format(1)
            if t.base_type_name == _get_fqcn(int):
                err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_INT
            elif t.base_type_name == _get_fqcn(bool):
                err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_BOOL
            logging.warning(err)

        t_parsed = self.at_ctx.api.analyze_type(t)

        if isinstance(t_parsed, TypeVarType):
            return t_parsed, TypeVar, False
        if isinstance(t_parsed, Instance):
            if t_parsed.type.name in dir(builtins):
                return t_parsed, eval(t_parsed.type.name), False
        elif isinstance(t_parsed, LiteralType):
            return t_parsed, t_parsed.value, False

        logging.warning(PARSE_TYPE_UNKNOWN_RAW_TYPE_WARNING.format(t_parsed))
        return t_parsed, None, False

    def validate_types(self, exp_types: List[object]) -> bool:
        """
        Validate that the given types correspond to a list of expected types.

        Additionally, we always accept when all type hints are TypeVars, since
        the Generic definition of the class is also type checked, e.g.,
        `Vector[U, V]` as return type of `Vector.copy()`.
        """

        # Trivially different
        if len(self.types) != len(exp_types):
            return False

        # Special case for all TypeVars
        if all([isinstance(t, TypeVarType) for t in self.types]):
            return True

        # Compare parsed types to expected types and return True iff all match
        return all([self.types_raw[i] == exp_types[i] for i in range(len(exp_types))])

    def validate_types_with_fn(self,
                               fn: Callable[..., bool],
                               allow_type_vars: bool = True) -> Union[bool, Tuple[bool, str]]:
        """
        Validate types with custom function, which is called on the recovered raw
        types of the input.

        The custom function returns a boolean which is true if the type are valid.
        Optionally, it can return a second value with an error message. 
        """

        if allow_type_vars and all([isinstance(t, TypeVarType) for t in self.types]):
            return True

        return fn(*self.types_raw)


def constraint(obj):
    """
    Decorator to add callable constraint to Constraints and process the
    AnalyzeTypeContext from mypy.plugin to a simpler ConstraintContext
    object.
    """
    def decorate(fn: Callable[[ConstraintContext], Union[bool, Tuple[bool, str]]]):
        fqcn = _get_fqcn(obj)

        def mypy_callback_wrapper(at_ctx: AnalyzeTypeContext) -> Type:
            constraint_ctx = ConstraintContext(at_ctx, obj)

            success = fn(constraint_ctx)
            type_args = constraint_ctx.types
            if not isinstance(type_args, list):
                type_args = list(type_args)

            err = DEFAULT_CONSTRAINT_FAILED_ERROR_MSG.format(fqcn, type_args)

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
