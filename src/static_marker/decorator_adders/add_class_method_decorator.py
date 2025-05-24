from __future__ import annotations

from collections.abc import Container

import libcst
from libcst import Attribute
from libcst import Name

from ._get_self_name import get_self_name
from ._makes_use_of_self import makes_use_of_self


def add_class_method_decorator(
    function_def: libcst.FunctionDef,
    static_or_class_method_names: Container[str],
) -> libcst.FunctionDef:
    self_name = get_self_name(function_def)
    if self_name is None:
        return function_def
    if function_def.decorators:
        return function_def
    if makes_use_of_self(function_def, static_or_class_method_names):
        return function_def
    function_def = function_def.with_changes(
        decorators=[
            libcst.Decorator(decorator=libcst.Name(classmethod.__name__))
        ]
    )
    params = function_def.params.with_changes(
        params=(function_def.params.params[0].with_changes(name=Name("cls")),)
        + function_def.params.params[1:]
    )
    function_def = _replace_self_with_cls(function_def, self_name)
    return function_def.with_changes(params=params)


def _replace_self_with_cls(
    function_def: libcst.FunctionDef, self_name: str
) -> libcst.FunctionDef:
    class SelfCallsGetter(libcst.CSTTransformer):

        def leave_Attribute(
            self, original_node: "Attribute", updated_node: "Attribute"
        ) -> "Attribute":
            if updated_node.value.value == self_name:
                return updated_node.with_changes(value=Name("cls"))
            return updated_node

    return function_def.visit(SelfCallsGetter())
