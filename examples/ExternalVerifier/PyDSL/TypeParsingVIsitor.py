import logging
import builtins

from typing import Tuple
from mypy.type_visitor import TypeQuery
from mypy.types import *

from PyDSL.Const import VISITOR_NOT_IMPLEMENTED

# def parse_type(self, t: Type) -> Tuple[Type, object, bool]:
#         if isinstance(t, RawExpressionType):
#             do_parse_raw_int = (self.allow_raw_int_types
#                                 and t.base_type_name == _get_fqcn(int))
#             do_parse_raw_bool = (self.allow_raw_bool_types
#                                  and t.base_type_name == _get_fqcn(bool))

#             if do_parse_raw_int or do_parse_raw_bool:
#                 t_raw = t.literal_value
#                 t_lit = LiteralType(
#                     value=t_raw,  # type: ignore
#                     fallback=self.at_ctx.api.named_type(t.base_type_name, [])
#                 )
#                 return t_lit, t_raw, True

#             err = PARSE_TYPE_UNEXPECTED_RAW.format(1)
#             if t.base_type_name == _get_fqcn(int):
#                 err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_INT
#             elif t.base_type_name == _get_fqcn(bool):
#                 err += PARSE_TYPE_UNEXPECTED_RAW_PRESUME_BOOL
#             logging.warning(err)

RetType = Tuple[Type, object, bool]

class TypeParsingVisitor(TypeQuery[RetType]):
    """
    Visitor class to parse the types into mypy types and raw types
    while tracking whether we used custom literal parsing at some point.
    """

    def visit_any(self, t: AnyType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_uninhabited_type(self, t: UninhabitedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_none_type(self, t: NoneType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_erased_type(self, t: ErasedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_deleted_type(self, t: DeletedType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_type_var(self, t: TypeVarType) -> RetType:
        r = self.query_types([t.upper_bound] + t.values)
        return t, TypeVar, False

    def visit_param_spec(self, t: ParamSpecType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_partial_type(self, t: PartialType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False
        
    def visit_instance(self, t: Instance) -> RetType:
        if t.type.name in dir(builtins):
            return t, eval(t.type.name), False
        
        return self.query_types(t.args)

    def visit_raw_expression_type(self, t: RawExpressionType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False

    def visit_literal_type(self, t: LiteralType) -> RetType:
        return t, t.value, False

    def visit_ellipsis_type(self, t: EllipsisType) -> RetType:
        logging.error(VISITOR_NOT_IMPLEMENTED)
        return AnyType(TypeOfAny.from_error), None, False
        
