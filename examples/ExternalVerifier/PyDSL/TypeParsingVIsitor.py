import logging
import builtins

from typing import Tuple, Callable
from mypy.type_visitor import TypeQuery
from mypy.types import *
from mypy.plugin import AnalyzeTypeContext

from PyDSL.Const import *
from PyDSL.InternalUtils import get_fqcn


RetType = Tuple[Type, object, bool]


class TypeParsingVisitor(TypeQuery[RetType]):
    """
    Visitor class to parse the types into mypy types and raw types
    while tracking whether we used custom literal parsing at some point.
    """

    def __init__(self,
                 at_ctx: AnalyzeTypeContext,
                 allow_raw_bool_types: bool,
                 allow_raw_int_types: bool,
                 strategy: Callable[[Iterable[RetType]], RetType]) -> None:

        self.at_ctx = at_ctx
        self.allow_raw_bool_types = allow_raw_bool_types
        self.allow_raw_int_types = allow_raw_int_types
        super().__init__(strategy)

    def visit_unbound_type(self, t: UnboundType) -> RetType:
        t_analyzed = self.at_ctx.api.analyze_type(t)
        return t_analyzed.accept(self)

    def visit_any(self, t: AnyType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(AnyType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_uninhabited_type(self, t: UninhabitedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(UninhabitedType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_none_type(self, t: NoneType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(NoneTyp))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_erased_type(self, t: ErasedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(ErasedType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_deleted_type(self, t: DeletedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(DeletedType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_type_var(self, t: TypeVarType) -> RetType:
        r = self.query_types([t.upper_bound] + t.values)
        return t, TypeVar, False

    def visit_param_spec(self, t: ParamSpecType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(ParamSpecType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_partial_type(self, t: PartialType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(PartialType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_instance(self, t: Instance) -> RetType:
        if t.type.name in dir(builtins):
            return t, eval(t.type.name), False

        return self.query_types(t.args)

    def visit_raw_expression_type(self, t: RawExpressionType) -> RetType:
        t_raw = t.literal_value

        err = PARSE_TYPE_UNEXPECTED_RAW.format(1)
        if t_raw == None:
            logging.error(err)
            return AnyType(TypeOfAny.from_error), None, False

        if self.allow_raw_int_types or self.allow_raw_bool_types:
            t_lit = LiteralType(
                value=t_raw,  # type: ignore
                fallback=self.at_ctx.api.named_type(t.base_type_name, [])
            )
            return t_lit, t_raw, True

        if t.base_type_name == get_fqcn(int):
            err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_INT
        elif t.base_type_name == get_fqcn(bool):
            err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_BOOL

        logging.error(err)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_literal_type(self, t: LiteralType) -> RetType:
        return t, t.value, False

    def visit_ellipsis_type(self, t: EllipsisType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(EllipsisType))
        return AnyType(TypeOfAny.from_error), None, False
