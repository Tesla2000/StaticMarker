from __future__ import annotations

import libcst

from ..config import Config


class Transformer(libcst.CSTTransformer):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config


class Visitor(libcst.CSTVisitor):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
