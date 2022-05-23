
import logging

from typing import Final, NoReturn
from mypy.plugin import Plugin, AnalyzeTypeContext
from mypy.types import (
    Type, AnyType, TypeOfAny
)

TYPE_NAME : Final = "MyListType.MyList"

class HecoPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str):
        print(fullname)
        if fullname == TYPE_NAME:
            return list_analyze_callback

def list_analyze_callback(ctx: AnalyzeTypeContext):
    ts = list(map(ctx.api.analyze_type, ctx.type.args))
    r = ctx.api.named_type(TYPE_NAME, ts)
    return r

def plugin(version: str):
    if version != "0.950":
        logging.warning(f"The custom HecoPlugin for MyPy was not tested with your MyPy version {version}.")
    return HecoPlugin
