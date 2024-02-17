# This file was generated automatically - do not edit manually

from typing import List

from classiq.qmod.qmod_parameter import QParam
from classiq.qmod.symbolic import symbolic_function

from .structs import *


def compute_qaoa_initial_point(
    hamiltonian: QParam[List[PauliTerm]],
    repetitions: QParam[int],
) -> QParam[List[float]]:
    return symbolic_function(hamiltonian, repetitions)


def molecule_problem_to_hamiltonian(
    problem: QParam[MoleculeProblem],
) -> QParam[List[PauliTerm]]:
    return symbolic_function(problem)


def fock_hamiltonian_problem_to_hamiltonian(
    problem: QParam[FockHamiltonianProblem],
) -> QParam[List[PauliTerm]]:
    return symbolic_function(problem)


def grid_entangler_graph(
    num_qubits: QParam[int],
    schmidt_rank: QParam[int],
    grid_randomization: QParam[bool],
) -> QParam[List[List[int]]]:
    return symbolic_function(num_qubits, schmidt_rank, grid_randomization)


def hypercube_entangler_graph(
    num_qubits: QParam[int],
) -> QParam[List[List[int]]]:
    return symbolic_function(num_qubits)


def log_normal_finance_post_process(
    finance_model: QParam[LogNormalModel],
    estimation_method: QParam[FinanceFunction],
    probability: QParam[float],
) -> QParam[float]:
    return symbolic_function(finance_model, estimation_method, probability)


def gaussian_finance_post_process(
    finance_model: QParam[GaussianModel],
    estimation_method: QParam[FinanceFunction],
    probability: QParam[float],
) -> QParam[float]:
    return symbolic_function(finance_model, estimation_method, probability)


__all__ = [
    "compute_qaoa_initial_point",
    "molecule_problem_to_hamiltonian",
    "fock_hamiltonian_problem_to_hamiltonian",
    "grid_entangler_graph",
    "hypercube_entangler_graph",
    "log_normal_finance_post_process",
    "gaussian_finance_post_process",
]
