
import logging
from sys import path
from os import environ

from typing import Final, List, Tuple
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import (
    AnyType, Instance, LiteralType, RawExpressionType, Type, TypeOfAny, 
    TypeVarType
)

from PyDSL.Constraints import Constraints
from PyDSL.Const import *
from PyDSL_Types import *

class PyDSLPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        for n, cb in Constraints().items():
            if fullname == n:
                return cb

def _is_builtins_int(t : Type) -> bool:
    return isinstance(t, Instance) and t.type.fullname == "builtins.int"

def _is_literal_int(t: Type) -> bool:
    return isinstance(t, RawExpressionType) and isinstance(t.literal_value, int)

def plugin(version: str):
    if version not in TESTED_VERSIONS:
        logging.warning(f"The custom HecoPlugin for MyPy was not tested with your MyPy version {version}.")
    
    return PyDSLPlugin
