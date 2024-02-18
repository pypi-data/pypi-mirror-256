
##  Usage
Quantum Gates
The module provides a variety of quantum gates essential for quantum computing simulations:

Pauli Gates:

X (Pauli-X)
Y (Pauli-Y)
Z (Pauli-Z)
Hadamard Gate (H):

A gate that creates superpositions by putting qubits into an equal superposition of |0⟩ and |1⟩ states.
Phase Gate (S):

Introduces a phase shift of π/2 to the |1⟩ state.
Rotation Gates (Rx, Ry, Rz):

Rotation around the x, y, and z axes by an angle θ.
Custom Gates:

rxx_matrix(phi): Custom two-qubit gate.
ryy_matrix(phi): Another custom two-qubit gate.

##  Advantages
Flexibility: The module supports a wide range of quantum gates, enabling the construction of complex quantum circuits for simulation.

Extensibility: Users can easily define and implement custom gates and operations, expanding the module's capabilities for various quantum computing experiments.

Compatibility: Designed to seamlessly work with other scientific computing libraries like NumPy and SciPy, providing a robust and efficient quantum simulation environment.

Educational Purpose: The module's clear and modular structure makes it suitable for educational purposes, aiding users in understanding the fundamentals of quantum computing.

## Example
                                                        \
    import qudoor as qd
    q0 = qd.Qubit([1, 0)] #initialyse the qubit of state |0>
    q1 = qd.Qubit([1, 0)]
    q0.apply_gate(qd.H) # apply the gate of Hazmare for the qubit 0
    q1.apply_gate(qd.Z) # another gate
    q0.apply_gate_two_qbit(q1, qd.CNOT_matrix) # apply the CNOT gate for the qubit 0 and qubit 1
    q0.normalize() # normalise the vector
    print(q0.mesure()) # mesure the vector
    # Be careful if you try to measure or display the probability of a qubit without normalising it, you could get an error.