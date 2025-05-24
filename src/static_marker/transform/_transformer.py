from __future__ import annotations

from typing import Optional

import libcst
from libcst import ClassDef
from libcst import FunctionDef
from libcst import Module

from ..config import Config


class Transformer(libcst.CSTTransformer):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self._methods: set[FunctionDef] = set()

    def leave_FunctionDef(
        self, original_node: "FunctionDef", updated_node: "FunctionDef"
    ) -> "FunctionDef":
        if original_node not in self._methods:
            return updated_node
        if (
            updated_node.params.params
            and updated_node.params.params[0].name.value
            in Module([updated_node.body]).code
        ):
            return updated_node
        if updated_node.decorators:
            return updated_node
        updated_node = updated_node.with_changes(
            decorators=[
                libcst.Decorator(decorator=libcst.Name("staticmethod"))
            ]
        )
        params = updated_node.params.with_changes(
            params=updated_node.params.params[1:]
        )
        updated_node = updated_node.with_changes(params=params)
        return updated_node

    def visit_ClassDef(self, node: "ClassDef") -> Optional[bool]:
        class MethodGetter(libcst.CSTVisitor):
            def visit_FunctionDef(
                _, function_node: "FunctionDef"
            ) -> Optional[bool]:
                self._methods.add(function_node)

        node.visit(MethodGetter())
        return super().visit_ClassDef(node)


class Visitor(libcst.CSTVisitor):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
