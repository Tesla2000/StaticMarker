from __future__ import annotations

import libcst

from ._get_self_name import get_self_name
from ._makes_use_of_self import makes_use_of_self


def add_static_method_decorator(
    function_def: libcst.FunctionDef,
) -> libcst.FunctionDef:
    if get_self_name(function_def) is None:
        return function_def
    if function_def.decorators:
        return function_def
    if makes_use_of_self(function_def, ()):
        return function_def
    function_def = function_def.with_changes(
        decorators=[
            libcst.Decorator(decorator=libcst.Name(staticmethod.__name__))
        ]
    )
    params = function_def.params.with_changes(
        params=function_def.params.params[1:]
    )
    return function_def.with_changes(params=params)
