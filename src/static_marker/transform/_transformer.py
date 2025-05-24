from __future__ import annotations

from typing import Optional

import libcst
from libcst import ClassDef
from libcst import FunctionDef

from ..config import Config
from ..decorator_adders.add_class_method_decorator import (
    add_class_method_decorator,
)
from ..decorator_adders.add_methods import add_methods
from ..decorator_adders.add_static_method_decorator import (
    add_static_method_decorator,
)


class Transformer(libcst.CSTTransformer):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self._methods: set[FunctionDef] = set()
        self._static_or_class_methods: set[FunctionDef] = set()

    def leave_FunctionDef(
        self, original_node: "FunctionDef", updated_node: "FunctionDef"
    ) -> "FunctionDef":
        if original_node not in self._methods:
            return updated_node
        if original_node in self._static_or_class_methods:
            return updated_node
        updated_node = add_static_method_decorator(updated_node)
        updated_node = add_class_method_decorator(
            updated_node, self._static_or_class_method_names
        )
        return updated_node

    @property
    def _static_or_class_method_names(self) -> frozenset[str]:
        return frozenset(
            method.name.value for method in self._static_or_class_methods
        )

    def visit_ClassDef(self, node: "ClassDef") -> Optional[bool]:
        add_methods(node, self._methods, self._static_or_class_methods)
        return super().visit_ClassDef(node)


class Visitor(libcst.CSTVisitor):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
