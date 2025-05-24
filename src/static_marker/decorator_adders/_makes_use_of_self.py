from __future__ import annotations

from collections.abc import Container
from typing import Optional

import libcst
from libcst import Attribute

from ._get_self_name import get_self_name


def makes_use_of_self(
    function_def: libcst.FunctionDef,
    static_or_class_method_names: Container[str],
) -> bool:
    self_name = get_self_name(function_def)

    class SelfCallsGetter(libcst.CSTVisitor):
        def visit_Attribute(self, node: "Attribute") -> Optional[bool]:
            if (
                node.value.value == self_name
                and node.attr.value not in static_or_class_method_names
            ):
                raise _SelfUsed
            return super().visit_Attribute(node)

    try:
        function_def.visit(SelfCallsGetter())
    except _SelfUsed:
        return True
    return False


class _SelfUsed(Exception):
    pass
