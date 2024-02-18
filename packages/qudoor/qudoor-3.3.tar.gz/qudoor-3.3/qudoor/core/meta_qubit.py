# myquantumlib/core/meta_qubit.py
from ast import literal_eval

import numpy as np
from matplotlib import pyplot as plt

from qudoor.core.constants import *


def get_P0(n):
    # Matrice identité pour un seul qubit
    I = np.eye(2)

    # Matrice identité pour le système de n qubits
    P0 = np.eye(n)

    return P0

class MetaQubit:
    def __init__(self, state=None):
        self.state = state
        self._array = None

    def apply_gate(self, gate_matrix):
        self._array = np.dot(self._array, gate_matrix)

    def apply_not(self):
        self.apply_gate(X)

    def apply_swap(self, other):
        self.apply_gate_two_qbit(other, CNOT_matrix)
        other.apply_gate_two_qbit(self, CNOT_matrix)
        self.apply_gate_two_qbit(other, CNOT_matrix)

    def apply_state(self, state):
        self.state = state
        self._array = np.array(state, dtype=np.complex128)  # Assurez-vous que le vecteur d'état est de type complexe
        self.apply_gate(I)
        return self

    def apply_gate_two_qbit(self, other, matrix):
        # Combinaison des états des deux qubits
        combined_state = np.kron(self._array, other._array)
        # Porte CNOT
        gate = matrix
        new_state = np.dot(gate, combined_state)
        # Extraire la matrice de l'état du qubit cible
        new_array, _ = np.split(new_state, 2, axis=0)
        self._array = new_array

    def mesure(self):
        try:
            # Probabilités d'observer les états |0⟩ et |1⟩
            probabilities = np.abs(self._array) ** 2

            # Éviter la division par zéro
            norm = np.sum(probabilities, dtype=np.int32)
            if norm != 0:
                probabilities /= norm
            else:
                self.probabilities = np.array([1, 0])
                if self._array == np.array([
                    0+0j, 0+0j
                ]):
                    return f"0 $ with the qubit Array:{self._array}"
                else:
                    return f"1 $ with the qubit Array:{self._array}"

            self.probabilities = np.array(probabilities)

            # Effectuer la mesure
            result = np.random.choice([0, 1], p=probabilities)

            # Mettre à jour l'état après la mesure
            self._array = np.array([1 if result == i else 0 for i in range(2)]).reshape(-1, 1)
            return f"{str(result)} $ with the qubit Array:{str(self._array)}"
        except:
            return f"0 $ with the qubit Array:{str(self._array)}"
def string_rep_states(n_qubits=3):
    state_strs = ['' for _ in range(2 ** n_qubits)]
    basis_strs = ['0', '1']

    for q in range(n_qubits):
        for i in range(len(state_strs)):
            b = basis_strs[(i // (2 ** q)) % 2]
            state_strs[i] = state_strs[i] + b

    return state_strs


def plt_measure_qubit(out_register_qubit):
    try:
        probabilities = np.abs(out_register_qubit._array) ** 2
        out_register = out_register_qubit._array
        n_qubits = int(np.log2(out_register.shape[0]))
        fig, ax = plt.subplots(1, 1)

        x_values = np.array(list(range(2 ** n_qubits)))
        out_register_qubit.mesure()
        ax.bar(x_values, probabilities)
        ax.set_xticks(x_values)
        ax.set_xticklabels(string_rep_states(n_qubits))
        ax.set_ylim(0, 1)
        ax.grid(True)
        ax.set_ylabel(r'$P(S_c)$')
        ax.set_xlabel(r'$S_c$')
        plt.show()
    except:
        raise TypeError("Impossible with a size if size is not a multiple of 4 or if size is 2")


def plt_measure_bit(out_register_qubit):
    out_register = out_register_qubit._array
    n_qubits = int(np.log2(out_register.shape[0]))
    fig, ax = plt.subplots(1, 1)
    x_values = np.array(list(range(2 ** n_qubits)))
    mesures = out_register_qubit.mesure()
    arraymesure = mesures.split(" $ ")[1].split(":")[1]
    armestr = arraymesure.split(" ")
    armes = armestr[0] + "," + armestr[1]
    ax.bar(x_values, np.array(literal_eval(armes)))
    ax.set_xticks(x_values)
    ax.set_xticklabels(string_rep_states(n_qubits))
    ax.set_ylim(0, 1)
    ax.grid(True)
    ax.set_ylabel(r'$P(S_c)$')
    ax.set_xlabel(r'$S_c$')
    plt.show()
