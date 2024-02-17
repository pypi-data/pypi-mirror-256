from sympy import Symbol

from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.model.quantum_type import QuantumNumeric


class QmodQNumProxy(Symbol, QmodSizedProxy):
    def __new__(cls, name, **assumptions):
        return super().__new__(cls, name, **assumptions)

    def __init__(self, name: str, quantum_type: QuantumNumeric) -> None:
        super().__init__(quantum_type.size_in_bits)
        self._fraction_digits = quantum_type.fraction_digits
        self._is_signed = quantum_type.is_signed

    @property
    def fraction_digits(self) -> int:
        return self._fraction_digits

    @property
    def is_signed(self) -> bool:
        return self._is_signed
