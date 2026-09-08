# ============================================================
# Session 2 Assignment: Qubit State Explorer
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from IPython.display import display


# ------------------------------------------------------------
# 1. Display available gates
# ------------------------------------------------------------

print("======================================")
print("       QUBIT STATE EXPLORER")
print("======================================")

print("\nAvailable Gates:")
print("1. X Gate")
print("2. Y Gate")
print("3. Z Gate")
print("4. H Gate")
print("5. RY Gate")


# ------------------------------------------------------------
# 2. Get user input
# ------------------------------------------------------------

choice = input("\nChoose a gate (1-5): ").strip()

# Create a quantum circuit with 1 qubit
qc = QuantumCircuit(1)

gate_name = ""


# ------------------------------------------------------------
# 3. Apply selected gate
# ------------------------------------------------------------

if choice == "1":
    qc.x(0)
    gate_name = "X Gate"

elif choice == "2":
    qc.y(0)
    gate_name = "Y Gate"

elif choice == "3":
    qc.z(0)
    gate_name = "Z Gate"

elif choice == "4":
    qc.h(0)
    gate_name = "H Gate"

elif choice == "5":

    theta = float(
        input("\nEnter rotation angle θ in radians: ")
    )

    qc.ry(theta, 0)
    gate_name = f"RY Gate (θ = {theta:.4f})"

else:
    print("\nInvalid choice. Please run the cell again and choose 1-5.")
    raise SystemExit


# ------------------------------------------------------------
# 4. Display the quantum circuit
# ------------------------------------------------------------

print("\n======================================")
print(f"Selected Gate: {gate_name}")
print("======================================")

print("\nQuantum Circuit:")

display(qc.draw("mpl"))


# ------------------------------------------------------------
# 5. Calculate the final quantum state
# ------------------------------------------------------------

state = Statevector.from_instruction(qc)

print("\nFinal Quantum State:")
print(state)


# ------------------------------------------------------------
# 6. Calculate measurement probabilities
# ------------------------------------------------------------

probabilities = state.probabilities()

prob_0 = probabilities[0]
prob_1 = probabilities[1]

print("\nMeasurement Probabilities:")
print(f"P(|0⟩) = {prob_0:.4f}  ({prob_0 * 100:.2f}%)")
print(f"P(|1⟩) = {prob_1:.4f}  ({prob_1 * 100:.2f}%)")


# ------------------------------------------------------------
# 7. Display Bloch Sphere
# ------------------------------------------------------------

print("\nBloch Sphere:")

display(plot_bloch_multivector(state))


# ------------------------------------------------------------
# 8. Display probability chart
# ------------------------------------------------------------

plt.figure(figsize=(6, 4))

plt.bar(
    ["|0⟩", "|1⟩"],
    [prob_0, prob_1]
)

plt.ylim(0, 1)
plt.ylabel("Probability")
plt.title(f"Measurement Probabilities - {gate_name}")

plt.show()