# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


"""Replace each sequence of Clifford gates by a single Clifford gate."""

from functools import partial

from qiskit.circuit import Instruction
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit.library import LinearFunction, PermutationGate
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.quantum_info.operators import Clifford
from qiskit.transpiler.passes import (
    CollectLinearFunctions,
    LinearFunctionsToPermutations,
)
from qiskit.transpiler.passes.optimization.collect_and_collapse import (
    CollectAndCollapse,
    collapse_to_operation,
    collect_using_filter_function,
)
from qiskit.transpiler.passes.utils import control_flow


class CollectCliffordsAsInstructions(CollectAndCollapse):
    """Collects blocks of Clifford gates and replaces them by a :class:`~qiskit.quantum_info.Clifford`
    object.
    """

    def __init__(
        self,
        do_commutative_analysis=False,
        split_blocks=True,
        min_block_size=2,
        split_layers=False,
        collect_from_back=False,
    ):
        """CollectCliffords initializer.

        Args:
            do_commutative_analysis (bool): if True, exploits commutativity relations
                between nodes.
            split_blocks (bool): if True, splits collected blocks into sub-blocks
                over disjoint qubit subsets.
            min_block_size (int): specifies the minimum number of gates in the block
                for the block to be collected.
            split_layers (bool): if True, splits collected blocks into sub-blocks
                over disjoint qubit subsets.
            collect_from_back (bool): specifies if blocks should be collected started
                from the end of the circuit.
        """

        collect_function = partial(
            collect_using_filter_function,
            filter_function=_is_clifford_gate,
            split_blocks=split_blocks,
            min_block_size=min_block_size,
            split_layers=split_layers,
            collect_from_back=collect_from_back,
        )
        collapse_function = partial(
            collapse_to_operation, collapse_function=_collapse_to_clifford
        )

        super().__init__(
            collect_function=collect_function,
            collapse_function=collapse_function,
            do_commutative_analysis=do_commutative_analysis,
        )


clifford_gate_names = [
    "x",
    "y",
    "z",
    "h",
    "s",
    "sdg",
    "cx",
    "cy",
    "cz",
    "swap",
    "clifford",
    "linear_function",
    "pauli",
]


def _is_clifford_gate(node):
    """Specifies whether a node holds a clifford gate."""
    return (
        node.op.name in clifford_gate_names
        and getattr(node.op, "condition", None) is None
    )


def _collapse_to_clifford(circuit):
    """Specifies how to construct a ``Clifford`` from a quantum circuit (that must
    consist of Clifford gates only)."""
    return Instruction("clifford", circuit.num_qubits, 0, [Clifford(circuit), circuit])


class CollectPermutations(CollectLinearFunctions):
    """Collect blocks of linear gates (:class:`.CXGate` and :class:`.SwapGate` gates)
    and replaces them by linear functions (:class:`.LinearFunction`)."""

    @control_flow.trivial_recurse
    def run(self, dag):
        """Run the CollectLinearFunctions pass on `dag`.
        Args:
            dag (DAGCircuit): the DAG to be optimized.
        Returns:
            DAGCircuit: the optimized DAG.
        """
        dag = super().run(dag)
        return self.linfunc_to_perm.run(dag)

    def __init__(
        self,
        do_commutative_analysis=False,
        split_blocks=True,
        min_block_size=2,
        split_layers=False,
        collect_from_back=False,
    ):
        """CollectLinearFunctions initializer.

        Args:
            do_commutative_analysis (bool): if True, exploits commutativity relations
                between nodes.
            split_blocks (bool): if True, splits collected blocks into sub-blocks
                over disjoint qubit subsets.
            min_block_size (int): specifies the minimum number of gates in the block
                for the block to be collected.
            split_layers (bool): if True, splits collected blocks into sub-blocks
                over disjoint qubit subsets.
            collect_from_back (bool): specifies if blocks should be collected started
                from the end of the circuit.
        """

        super().__init__(
            do_commutative_analysis,
            split_blocks,
            min_block_size,
            split_layers,
            collect_from_back,
        )

        self.collect_function = partial(
            collect_using_filter_function,
            filter_function=_is_permutation_gate,
            split_blocks=split_blocks,
            min_block_size=min_block_size,
            split_layers=split_layers,
            collect_from_back=collect_from_back,
        )

        self.linfunc_to_perm = LinearFunctionsToPermutations()


def _is_permutation_gate(node):
    """Specifies whether a node holds a swap gate."""
    return node.op.name in ("swap") and getattr(node.op, "condition", None) is None
