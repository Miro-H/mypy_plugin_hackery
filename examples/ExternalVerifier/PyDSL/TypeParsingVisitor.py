import logging
import builtins

from typing import Tuple, Callable
from mypy.types import *
from mypy.plugin import AnalyzeTypeContext

from PyDSL.Const import *
from PyDSL.CustomTypes import rewrite_literal
from PyDSL.InternalUtils import get_fqcn


RetType = Tuple[Type, Optional[list]]


class TypeParsingVisitor(TypeQuery[RetType]):
    """
    Visitor class to parse the types into mypy types and raw types
    while tracking whether we used custom literal parsing at some point.
    """

    def __init__(self,
                 at_ctx: AnalyzeTypeContext,
                 strategy: Callable[[Iterable[RetType]], RetType]) -> None:

        self.at_ctx = at_ctx
        super().__init__(strategy)

    def visit_unbound_type(self, t: UnboundType) -> RetType:
        t_analyzed = self.at_ctx.api.analyze_type(t)
        
        # Restore unanalyzed arguments if relevant (otherwise we might loose raw literals)
        if hasattr(t_analyzed, "args"):
            t_analyzed.args = type(t_analyzed.args)(t.args) # type: ignore

        # Avoid infinite recursion by leaving unbounded variables unbounded if they cannot
        # be further resolved.
        if type(t_analyzed) != UnboundType:
            return t_analyzed.accept(self)

        return t, list(t.args)

    def visit_any(self, t: AnyType) -> RetType:
        return t, None
        
    def visit_uninhabited_type(self, t: UninhabitedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(UninhabitedType))
        return AnyType(TypeOfAny.from_error), None

    def visit_none_type(self, t: NoneType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(NoneTyp))
        return AnyType(TypeOfAny.from_error), None

    def visit_erased_type(self, t: ErasedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(ErasedType))
        return AnyType(TypeOfAny.from_error), None

    def visit_deleted_type(self, t: DeletedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(DeletedType))
        return AnyType(TypeOfAny.from_error), None

    def visit_type_var(self, t: TypeVarType) -> RetType:
        r = self.query_types([t.upper_bound] + t.values)
        return t, [TypeVar]

    def visit_param_spec(self, t: ParamSpecType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(ParamSpecType))
        return AnyType(TypeOfAny.from_error), None

    def visit_partial_type(self, t: PartialType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(PartialType))
        return AnyType(TypeOfAny.from_error), None

    def visit_instance(self, t: Instance) -> RetType:
        if t.type.name in dir(builtins):
            return t, [eval(t.type.name)]

        args_list, args_raw = self.query_types(t.args)

        if hasattr(args_list, "__iter__"):
            args_tpl = tuple(args_list) # type: ignore
        else:
            args_tpl = (args_list,)
        t.args = args_tpl
        return t, args_raw

    def visit_raw_expression_type(self, t: RawExpressionType) -> RetType:
        t_raw = t.literal_value

        err = PARSE_TYPE_UNEXPECTED_RAW.format(t)
        if t_raw == None:
            logging.error(err)
            return AnyType(TypeOfAny.from_error), None

        return t, [t_raw]

    def visit_literal_type(self, t: LiteralType) -> RetType:
        return t, [t.value]

    def visit_ellipsis_type(self, t: EllipsisType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(EllipsisType))
        return AnyType(TypeOfAny.from_error), None
