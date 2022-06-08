import logging
import traceback
from PyDSL.CustomTypes import rewrite_literals

from PyDSL.TypeParsingVisitor import TypeParsingVisitor
from PyDSL.InternalUtils import get_fqcn

from .Const import *

from typing import Callable, Dict, List, Union, Tuple, Optional, Final
from mypy.types import AnyType, Type, TypeOfAny, TypeVarType, UnionType, RawExpressionType, LiteralType, NoneType
from mypy.plugin import AnalyzeTypeContext, AttributeContext


class Constraints(object):
    """
    Internal structure storing all registered constraints.
    Register a new constraint with the decorators @*_constraint.
    """

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._class_constraints: Dict[str, Callable] = dict()
            cls._attributes_constraints: Dict[str, Callable] = dict()
            cls.instance = super(Constraints, cls).__new__(cls)
        return cls.instance

    def add_class_constraint(self, key: str, item: Callable) -> None:
        if key in self._class_constraints:
            logging.warning(CONSTRAINTS_OVERWRITING_WARNING.format(key))
        self._class_constraints[key] = item

    def get_class_constraint(self, key: str) -> Callable:
        return self._class_constraints[key]

    def get_class_constraints(self) -> Dict[str, Callable]:
        return self._class_constraints

    def add_attributes_constraint(self, key: str, item: Callable) -> None:
        if key in self._class_constraints:
            logging.warning(CONSTRAINTS_OVERWRITING_WARNING.format(key))
        self._attributes_constraints[key] = item

    def get_attributes_constraint(self, key: str) -> Callable:
        return self._attributes_constraints[key]

    def get_attributes_constraints(self) -> Dict[str, Callable]:
        return self._attributes_constraints


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

        # Analyze types of arguments and convert builtin.{int,bool} literals `a`
        # to `Literal[a]` if custom literal parsing is active.
        self.types = []
        self.types_raw = []

        def make_literal_type(e: RawExpressionType):
            val = e.literal_value
            if val:
                return LiteralType(
                    value=val,
                    fallback=at_ctx.api.named_type(e.base_type_name, [])
                )
            else:
                return NoneType()

        args = rewrite_literals(obj, make_literal_type, at_ctx.type.args)
        for arg in args:
            t_parsed, t_raw = self.parse_type(arg)
            self.types.append(t_parsed)
            self.types_raw.append(t_raw)
        
    def parse_type(self, t: Type) -> Tuple[Type, Optional[list]]:
        def strategy(results):
            ret_parsed = []
            ret_raw = []

            for parsed, raw in results:
                ret_parsed.append(parsed)
                if raw:
                    ret_raw += raw

            if len(ret_parsed) > 1:
                ret_parsed = UnionType(ret_parsed)

            return ret_parsed, ret_raw

        visitor = TypeParsingVisitor(self.at_ctx, strategy)
        return t.accept(visitor)

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

        # Catch missing raw types
        if any([type_raw == None for type_raw in self.types_raw]):
            logging.error(VALIDATE_TYPE_MISSING_RAW)
            return False

        # Unpack single arguments
        types_raw_unpacked = []
        for type_raw in self.types_raw:
            if isinstance(type_raw, list) and len(type_raw) == 1:
                types_raw_unpacked.append(type_raw[0])
            else:
                types_raw_unpacked.append(type_raw)

        return fn(*types_raw_unpacked)


class AttributeConstraintContext:
    """
    This class holds context that is useful to evaluate if an attribute
    is valid or not.

    Attributes:
        type : Type; MyPy type of the attribute

        ctx : AttributeContext;    The full context provided by MyPy to
                                        the attribute analyzing hooks.
    """

    def __init__(self, ctx: AttributeContext) -> None:
        self.type = ctx.default_attr_type


def class_constraint(obj):
    """
    Decorator to add callable constraint to Constraints and process the
    AnalyzeTypeContext from mypy.plugin to a simpler ConstraintContext
    object.
    """
    def decorate(fn: Callable[[ConstraintContext], Union[bool, Tuple[bool, str]]]):
        fqcn = get_fqcn(obj)

        def mypy_callback_wrapper(at_ctx: AnalyzeTypeContext) -> Type:
            constraint_ctx = ConstraintContext(at_ctx, obj)

            type_args = constraint_ctx.types
            if not isinstance(type_args, list):
                type_args = list(type_args)
            err = CONSTRAINT_DEFAULT_FAILED_ERROR_MSG.format(fqcn, type_args)

            try:
                success = fn(constraint_ctx)
            except Exception as e:
                logging.error(CONSTRAINT_CUSTOM_FN_FAILED_MSG.format(
                    fqcn, repr(e), traceback.format_exc()))
                err = CONSTRAINT_CUSTOM_FN_FAILED_SHORT_MSG.format(fqcn)
                success = False

            if isinstance(success, tuple):
                success, err = success

            if success:
                return at_ctx.api.named_type(fqcn, constraint_ctx.types)
            else:
                at_ctx.api.fail(err, at_ctx.context)
                return AnyType(TypeOfAny.from_error)

        Constraints().add_class_constraint(fqcn, mypy_callback_wrapper)

        return mypy_callback_wrapper

    return decorate


def attribute_constraint(obj, outer_attrs: List[str] = None):
    """
    Decorator to add callable attribute constraints to Constraints and process the
    AnalyzeTypeContext from mypy.plugin to a simpler ConstraintContext
    object.

    If attributes are specified in attrs, the function only applies to them. By
    default, it applies to all attributes of the class.
    """

    def decorate(fn: Callable[[AttributeConstraintContext], Union[bool, Tuple[bool, str]]]):
        fqcn = get_fqcn(obj)

        # Heuristically add all attributes. Assumes no user attribute starts with two underlines.
        if not outer_attrs:
            attrs: List[str] = []
            if hasattr(obj, "__annotations__"):
                attrs += obj.__annotations__.keys()
            if hasattr(obj, "__dict__"):
                attrs += list(filter(lambda x: not x.startswith("__"),
                              obj.__dict__.keys()))
            attrs = list(set(attrs))
        else:
            attrs = outer_attrs

        def mypy_callback_wrapper(ctx: AttributeContext) -> Type:
            attr_ctx = AttributeConstraintContext(ctx)
            success = fn(attr_ctx)

            err = ATTRIBUTE_CONSTRAINT_DEFAULT_FAILED_ERROR_MSG.format(
                fqcn, ctx.default_attr_type)

            if isinstance(success, tuple):
                success, err = success

            if success:
                return ctx.default_attr_type
            else:
                ctx.api.fail(err, ctx.context)
                return AnyType(TypeOfAny.from_error)

        for a in attrs:
            Constraints().add_attributes_constraint(
                f"{fqcn}.{a}", mypy_callback_wrapper)

        return mypy_callback_wrapper

    return decorate
