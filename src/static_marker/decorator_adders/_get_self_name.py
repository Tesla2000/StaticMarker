from __future__ import annotations

from functools import lru_cache
from typing import Optional

from libcst import FunctionDef


@lru_cache
def get_self_name(function_def: "FunctionDef") -> Optional[str]:
    if not function_def.params.params:
        return None
    return function_def.params.params[0].name.value
