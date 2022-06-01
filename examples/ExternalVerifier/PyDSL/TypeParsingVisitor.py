import logging
import builtins

from typing import Tuple, Callable
from mypy.types import *
from mypy.plugin import AnalyzeTypeContext

import PyDSL
from PyDSL.Const import *
from PyDSL.CustomTypes import rewrite_literal
from PyDSL.InternalUtils import get_fqcn


RetType = Tuple[Type, Optional[list], bool]


class TypeParsingVisitor(TypeQuery[RetType]):
    """
    Visitor class to parse the types into mypy types and raw types
    while tracking whether we used custom literal parsing at some point.
    """

    def __init__(self,
                 at_ctx: AnalyzeTypeContext,
                 strategy: Callable[[Iterable[RetType]], RetType]) -> None:

        self.at_ctx = at_ctx
        self.raw_literal_name: Any = None
        super().__init__(strategy)

    def visit_unbound_type(self, t: UnboundType) -> RetType:
        t_analyzed = self.at_ctx.api.analyze_type(t)
        
        # Restore unanalyzed arguments if relevant (otherwise we might loose raw literals)
        if hasattr(t_analyzed, "args"):
            t_analyzed.args = t.args # type: ignore

        # Avoid infinite recursion by leaving unbounded variables unbounded if they cannot
        # be further resolved.
        if type(t_analyzed) != UnboundType:
            return t_analyzed.accept(self)

        return t, list(t.args), False

    def visit_any(self, t: AnyType) -> RetType:
        return t, None, False

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
        return t, [TypeVar], False

    def visit_param_spec(self, t: ParamSpecType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(ParamSpecType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_partial_type(self, t: PartialType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(PartialType))
        return AnyType(TypeOfAny.from_error), None, False

    def visit_instance(self, t: Instance) -> RetType:
        if t.type.name in dir(builtins):
            return t, eval(t.type.name), False

        # TODO: fix this for xDSL
        if t.type.fullname.startswith("PyDSL.CustomTypes"):
            self.raw_literal_name = t.type.fullname

        print("VISIT INSTANCE", t)
        args_list, args_raw, custom_parsed = self.query_types(t.args)
        
        self.raw_literal_name = None

        # Unwarp query_types response
        if isinstance(args_raw, list) and isinstance(args_list, list):
            if len(args_list) > 1 or len(args_list) != len(args_raw):
                logging.error(VISITOR_INSTANCE_UNEXPECTED_ARGS_NR.format(args_list))
            elif len(args_list) == 1:
                args_raw = args_raw[0]
                args_list = args_list[0]
        else:
            logging.error(VISITOR_INSTANCE_EXPECTED_LIST.format(args_list, args_raw))

        print("ret", args_list, args_raw, type(args_list), type(args_raw))
        return args_list, args_raw, custom_parsed

    def visit_raw_expression_type(self, t: RawExpressionType) -> RetType:
        t_raw = t.literal_value

        err = PARSE_TYPE_UNEXPECTED_RAW.format(t)
        if t_raw == None:
            logging.error(err)
            return AnyType(TypeOfAny.from_error), None, False

        # t_lit = rewrite_literal(self.class_obj, t_raw)

        # if t_lit != t_raw:
        return t, [t_raw], False
        # if self.raw_literal_name:
        #     lit : Type 
        #     if not t_raw:
        #         lit = NoneType()
        #     else:
        #         lit = LiteralType(
        #             value=t_raw,
        #             fallback=self.at_ctx.api.named_type(t.base_type_name, [])
        #         )

        #     t_lit = self.at_ctx.api.named_type(self.raw_literal_name, [lit])
        #     print("derived raw:", t_lit)
        #     return t_lit, [t_raw], True

        # if t.base_type_name == get_fqcn(int):
        #     err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_INT
        # elif t.base_type_name == get_fqcn(bool):
        #     err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_BOOL

        # logging.error(err)
        # return AnyType(TypeOfAny.from_error), None, False

    def visit_literal_type(self, t: LiteralType) -> RetType:
        return t, [t.value], False

    def visit_ellipsis_type(self, t: EllipsisType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED.format(EllipsisType))
        return AnyType(TypeOfAny.from_error), None, False
