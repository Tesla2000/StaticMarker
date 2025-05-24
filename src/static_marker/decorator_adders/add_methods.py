from __future__ import annotations

import libcst
from libcst import ClassDef
from libcst import FunctionDef


def add_methods(
    class_def: ClassDef,
    methods: set[FunctionDef],
    static_or_class_methods: set[FunctionDef],
) -> None:
    def add_method(function_node: "FunctionDef") -> None:
        methods.add(function_node)
        decorator_names = frozenset(
            decorator.decorator.value
            for decorator in function_node.decorators
            if isinstance(decorator.decorator, libcst.Name)
        )
        if (
            staticmethod.__name__ in decorator_names
            or classmethod.__name__ in decorator_names
        ):
            static_or_class_methods.add(function_node)

    tuple(
        map(
            add_method,
            filter(FunctionDef.__instancecheck__, class_def.body.body),
        )
    )
