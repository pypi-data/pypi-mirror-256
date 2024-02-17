import ast
import inspect
import sys
from textwrap import dedent
from typing import Callable

from classiq.exceptions import ClassiqValueError
from classiq.qmod.builtins.classical_execution_primitives import sample, save


def _unparse_function_body(code: str, func: ast.FunctionDef) -> str:
    first_statement = func.body[0]
    body_lines = list(code.split("\n"))[first_statement.lineno - 1 :]
    body_lines[0] = body_lines[0][first_statement.col_offset :]
    if len(body_lines) > 1:
        body_lines = [body_lines[0], dedent("\n".join(body_lines[1:]))]
    return "\n".join(body_lines).strip()


class CFunc:
    @staticmethod
    def default_cmain() -> "CFunc":
        @CFunc
        def cmain() -> None:
            result = sample()
            save({"result": result})

        return cmain

    def __init__(self, py_callable: Callable[[], None]):
        code = dedent(inspect.getsource(py_callable))
        func = ast.parse(code).body[0]
        if not isinstance(func, ast.FunctionDef):
            raise ClassiqValueError(f"Use @{CFunc.__name__} to decorate a function")
        if len(func.args.args) > 0:
            raise ClassiqValueError(f"A @{CFunc.__name__} must receive no arguments")
        if sys.version_info >= (3, 9):
            self.code = "\n".join([ast.unparse(statement) for statement in func.body])
        else:
            self.code = _unparse_function_body(code, func)
