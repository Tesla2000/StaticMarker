from __future__ import annotations

from typing import Optional

import libcst
from libcst import ClassDef
from libcst import FunctionDef


def add_methods(
    class_def: ClassDef,
    methods: set[FunctionDef],
    static_or_class_methods: set[FunctionDef],
):
    class MethodGetter(libcst.CSTVisitor):
        def visit_FunctionDef(
            self, function_node: "FunctionDef"
        ) -> Optional[bool]:
            methods.add(function_node)
            decorator_names = frozenset(
                decorator.decorator.value
                for decorator in function_node.decorators
            )
            if (
                staticmethod.__name__ in decorator_names
                or classmethod.__name__ in decorator_names
            ):
                static_or_class_methods.add(function_node)
            return super().visit_FunctionDef(function_node)

    class_def.visit(MethodGetter())
