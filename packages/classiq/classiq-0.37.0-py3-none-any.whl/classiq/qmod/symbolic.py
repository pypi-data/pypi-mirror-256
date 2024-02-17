import sys
from typing import Tuple

from classiq.qmod.qmod_parameter import QParamScalar
from classiq.qmod.symbolic_expr import SymbolicExpr
from classiq.qmod.symbolic_type import SymbolicTypes

pi = SymbolicExpr("pi")
E = SymbolicExpr("E")
I = SymbolicExpr("I")  # noqa: E741
GoldenRatio = SymbolicExpr("GoldenRatio")
EulerGamma = SymbolicExpr("EulerGamma")
Catalan = SymbolicExpr("Catalan")


def symbolic_function(*args: SymbolicTypes) -> QParamScalar:
    str_args = [str(x) for x in args]
    return QParamScalar(f"{sys._getframe(1).f_code.co_name}({','.join(str_args)})")


def sin(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def cos(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def tan(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def cot(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def sec(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def csc(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def asin(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def acos(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def atan(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def acot(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def asec(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def acsc(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def sinh(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def cosh(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def tanh(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def coth(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def sech(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def csch(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def asinh(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def acosh(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def atanh(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def acoth(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def asech(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def exp(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def log(x: SymbolicTypes, base: SymbolicTypes = E) -> QParamScalar:
    return symbolic_function(x, base)


def ln(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def sqrt(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def abs(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def floor(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def ceiling(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def erf(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def erfc(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def gamma(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def beta(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def besselj(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def bessely(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def besseli(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def besselk(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def dirichlet_eta(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def polygamma(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def loggamma(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def factorial(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def binomial(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def subfactorial(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def primorial(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def bell(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def bernoulli(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def euler(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def catalan(x: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x)


def Piecewise(*args: Tuple[SymbolicTypes, SymbolicTypes]) -> QParamScalar:  # noqa: N802
    return symbolic_function(*args)


def max(x: SymbolicTypes, y: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x, y)


def min(x: SymbolicTypes, y: SymbolicTypes) -> QParamScalar:
    return symbolic_function(x, y)


def logical_and(x: SymbolicTypes, y: SymbolicTypes) -> SymbolicExpr:
    return SymbolicExpr._binary_op(x, y, "and")


def logical_or(x: SymbolicTypes, y: SymbolicTypes) -> SymbolicExpr:
    return SymbolicExpr._binary_op(x, y, "or")


def logical_not(x: SymbolicTypes) -> SymbolicExpr:
    return SymbolicExpr._unary_op(x, "not")


__all__ = [
    "pi",
    "E",
    "I",
    "GoldenRatio",
    "EulerGamma",
    "Catalan",
    "sin",
    "cos",
    "tan",
    "cot",
    "sec",
    "csc",
    "asin",
    "acos",
    "atan",
    "acot",
    "asec",
    "acsc",
    "sinh",
    "cosh",
    "tanh",
    "coth",
    "sech",
    "csch",
    "asinh",
    "acosh",
    "atanh",
    "acoth",
    "asech",
    "exp",
    "log",
    "ln",
    "sqrt",
    "abs",
    "floor",
    "ceiling",
    "erf",
    "erfc",
    "gamma",
    "beta",
    "besselj",
    "bessely",
    "besseli",
    "besselk",
    "dirichlet_eta",
    "polygamma",
    "loggamma",
    "factorial",
    "binomial",
    "subfactorial",
    "primorial",
    "bell",
    "bernoulli",
    "euler",
    "catalan",
    "Piecewise",
    "max",
    "min",
    "logical_and",
    "logical_or",
    "logical_not",
]


def __dir__():
    return __all__
