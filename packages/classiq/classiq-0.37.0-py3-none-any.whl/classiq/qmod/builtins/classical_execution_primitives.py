from typing import Dict, List, Optional

from classiq.interface.executor.execution_preferences import QaeWithQpeEstimationMethod
from classiq.interface.executor.iqae_result import IQAEResult
from classiq.interface.executor.result import EstimationResult, ExecutionDetails
from classiq.interface.executor.vqe_result import VQESolverResult
from classiq.interface.generator.expressions.enums import Optimizer
from classiq.interface.generator.functions.qmod_python_interface import QmodPyStruct
from classiq.interface.generator.types.combinatorial_problem import (
    CombinatorialOptimizationStructDeclaration,
)

from classiq.applications.qsvm.qsvm import Data, Labels

ExecutionParams = Dict[str, float]


def save(values_to_save: dict) -> None:
    pass


def sample(  # type: ignore
    execution_params: Optional[ExecutionParams] = None,
) -> ExecutionDetails:
    pass


def estimate(  # type: ignore
    hamiltonian: List[QmodPyStruct], execution_params: Optional[ExecutionParams] = None
) -> EstimationResult:
    pass


def vqe(  # type: ignore
    hamiltonian: List[QmodPyStruct],
    maximize: bool,
    initial_point: List[int],
    optimizer: Optimizer,
    max_iteration: int,
    tolerance: float,
    step_size: float,
    skip_compute_variance: bool,
    alpha_cvar: float,
) -> VQESolverResult:
    pass


def qae_with_qpe_result_post_processing(  # type: ignore
    estimation_register_size: int,
    estimation_method: QaeWithQpeEstimationMethod,
    result: ExecutionDetails,
) -> float:
    pass


def qsvm_full_run(  # type: ignore
    train_data: Data,
    train_labels: Labels,
    test_data: Data,
    test_labels: Labels,
    predict_data: Data,
) -> QmodPyStruct:
    pass


def iqae(  # type: ignore
    epsilon: float,
    alpha: float,
    execution_params: Optional[ExecutionParams] = None,
) -> IQAEResult:
    pass


def molecule_ground_state_solution_post_process(  # type: ignore
    problem: QmodPyStruct, vqe_result: VQESolverResult
) -> QmodPyStruct:
    pass


def optimization_problem_to_hamiltonian(  # type: ignore
    problem_struct: CombinatorialOptimizationStructDeclaration, penalty_energy: float
) -> List[QmodPyStruct]:
    pass


def get_optimization_solution(  # type: ignore
    problem_struct: CombinatorialOptimizationStructDeclaration,
    vqe_result: VQESolverResult,
    penalty_energy: float,
) -> List[QmodPyStruct]:
    pass


__all__ = [
    "save",
    "sample",
    "estimate",
    "vqe",
    "qae_with_qpe_result_post_processing",
    "qsvm_full_run",
    "iqae",
    "molecule_ground_state_solution_post_process",
    "optimization_problem_to_hamiltonian",
    "get_optimization_solution",
]


def __dir__() -> List[str]:
    return __all__
