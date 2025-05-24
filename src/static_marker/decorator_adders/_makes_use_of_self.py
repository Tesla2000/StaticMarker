from __future__ import annotations

from collections.abc import Container
from typing import Optional

import libcst
from libcst import Attribute
from libcst import Name

from ._get_self_name import get_self_name


def makes_use_of_self(
    function_def: libcst.FunctionDef,
    static_or_class_method_names: Container[str],
) -> bool:
    self_name = get_self_name(function_def)

    class SelfCallsGetter(libcst.CSTVisitor):
        def __init__(self) -> None:
            super().__init__()
            self._attribute_names: set[Name] = set()

        def visit_Attribute(self, node: "Attribute") -> Optional[bool]:
            name = node.value
            if not isinstance(name, Name):
                return super().visit_Attribute(node)
            if (
                name.value == self_name
                and node.attr.value not in static_or_class_method_names
            ):
                raise _SelfUsed
            self._attribute_names.add(name)
            return super().visit_Attribute(node)

        def visit_Name(self, node: "Name") -> Optional[bool]:
            if node in self._attribute_names:
                return super().visit_Name(node)
            if node.value in (self_name, super.__name__):
                raise _SelfUsed
            return super().visit_Name(node)

    try:
        function_def.body.visit(SelfCallsGetter())
    except _SelfUsed:
        return True
    return False


class _SelfUsed(Exception):
    pass
