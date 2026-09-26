"""
Assignment 3 — Quantum Pattern Search

Searches an 8-element space of 3-bit patterns using Grover's algorithm.

The target pattern is provided by the user, and the oracle is built dynamically.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt


NUM_QUBITS = 3
SHOTS = 1024
NUM_GROVER_ITERATIONS = 2


def apply_oracle(qc: QuantumCircuit, target: str) -> None:
    """
    Mark the target state with a phase flip.

    The target is supplied dynamically, so this oracle works for all
    3-bit patterns from 000 through 111.
    """
    # Qiskit's q0 corresponds to the rightmost bit of a measured
    # computational-basis string.
    target_reversed = target[::-1]

    # Convert the target state to |111>.
    for qubit, bit in enumerate(target_reversed):
        if bit == "0":
            qc.x(qubit)

    # H-X-H on the target qubit implements a Z phase flip,
    # controlled by q0 and q1 through the MCX operation.
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)

    # Restore the original basis mapping.
    for qubit, bit in enumerate(target_reversed):
        if bit == "0":
            qc.x(qubit)


def apply_diffuser(qc: QuantumCircuit) -> None:
    """Apply the 3-qubit Grover diffusion operator."""
    qc.h(range(NUM_QUBITS))
    qc.x(range(NUM_QUBITS))

    # Phase flip of |111>.
    qc.h(2)
    qc.mcx([0, 1], 2)
    qc.h(2)

    qc.x(range(NUM_QUBITS))
    qc.h(range(NUM_QUBITS))


def build_grover_circuit(target: str) -> QuantumCircuit:
    """Build the complete Grover circuit for the selected target."""
    qc = QuantumCircuit(NUM_QUBITS)

    # 1. Create equal superposition of all 8 states.
    qc.h(range(NUM_QUBITS))

    # 2. Oracle + diffuser.
    for _ in range(NUM_GROVER_ITERATIONS):
        apply_oracle(qc, target)
        apply_diffuser(qc)

    return qc


def validate_target(target: str) -> bool:
    """Return True when target is a valid 3-bit binary pattern."""
    return len(target) == 3 and all(bit in "01" for bit in target)


def main() -> None:
    search_space = [format(i, "03b") for i in range(2**NUM_QUBITS)]

    print("=" * 60)
    print("             QUANTUM PATTERN SEARCH")
    print("=" * 60)

    print("\nSearch space:")
    print(" ".join(search_space))

    target = input("\nEnter target pattern (000-111): ").strip()

    if not validate_target(target):
        print("\nInvalid target.")
        print("Please enter exactly 3 binary digits, for example: 101")
        return

    print(f"\nTarget pattern: {target}")
    print(f"Grover iterations: {NUM_GROVER_ITERATIONS}")

    # Build Grover circuit.
    grover = build_grover_circuit(target)

    print("\nQuantum Circuit:")
    print(grover.draw("text"))

    # Exact statevector before measurement.
    state = Statevector.from_instruction(grover)

    print("\nFinal Statevector:")
    print(state)

    # Add measurement only to the circuit used for simulation.
    measured_circuit = grover.copy()
    measured_circuit.measure_all()

    simulator = AerSimulator()

    result = simulator.run(
        measured_circuit,
        shots=SHOTS
    ).result()

    counts = result.get_counts()

    print("\nMeasurement Counts:")
    print(counts)

    identified_pattern = max(counts, key=counts.get)
    target_count = counts.get(target, 0)
    success_rate = target_count / SHOTS * 100

    print("\n" + "=" * 60)
    print("                    RESULT")
    print("=" * 60)
    print(f"Target pattern:       {target}")
    print(f"Identified pattern:   {identified_pattern}")
    print(f"Target measurements:  {target_count} / {SHOTS}")
    print(f"Target success rate:  {success_rate:.2f}%")
    print("=" * 60)

    if identified_pattern == target:
        print("Target pattern successfully identified.")
    else:
        print("The target was not the most frequent result in this run.")

    # Display histogram.
    plot_histogram(
        counts,
        title=f"Grover Search — Target: {target}"
    )
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
