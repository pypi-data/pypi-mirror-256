# myquantumlib/core/meta_qubit.py
from ast import literal_eval

import numpy as np

from qudoor.core.gate import *
from matplotlib import pyplot as plt

from qudoor.core.constants import *
from functools import reduce

def get_P0(n):
    # Matrice identité pour un seul qubit
    I = np.eye(2)

    # Matrice identité pour le système de n qubits
    P0 = np.eye(n)

    return P0

def get_matrix_with_result(result):
    if result == 0:
        return np.array([1, 0])
    else:
        return np.array([0, 1])

class MetaQubit:
    def __init__(self, state=None):
        self.state = state
        self._array = None

    def normalize(self):
        norm = np.linalg.norm(self._array)
        if norm != 0:
            self._array = self._array / norm

    def apply_gate(self, gate):
        gateclass = gate([self])
        gateclass.apply(0, 0)
        self._array = gateclass.retQbit(0)._array
        self.normalize()


    def apply_not(self):
        gateclass = XGate([self])
        gateclass.apply(0, 0)
        self._array = gateclass.retQbit(0)._array
        self.normalize()

    def apply_swap(self, other):
        self.apply_gate_two_qbit(other, CXGate)
        other.apply_gate_two_qbit(self, CXGate)
        self.apply_gate_two_qbit(other, CXGate)

    def apply_state(self, state):
        self.state = state
        self._array = np.array(state, dtype=np.complex128)  # Assurez-vous que le vecteur d'état est de type complexe
        return self

    def apply_gate_two_qbit(self, other, gate):
        gateclass = gate([self, other])
        gateclass.apply(1, 0)
        self._array = gateclass.retQbit(0)._array
        self.normalize()

    def apply_gate_three_gubit(self, other1, other2, gate):
        gateclass = gate([self, other1, other2])
        gateclass.apply([0, 1], 2)
        self._array = gateclass.retQbit(2)._array
        self.normalize()


    def mesure(self):
        self._project_pauli_z()
        probabilities = np.abs(self._array) ** 2
        result = np.random.choice([0, 1], p=probabilities)
        # Mettre à jour le vecteur d'état après la mesure
        array = self._array
        new_state = np.zeros_like(self._array, dtype=np.complex128)
        new_state[result] = 1
        self._array = new_state / np.sqrt(np.sum(np.abs(new_state) ** 2))

        return f"{result} $ with the qubit Array:{str(array)}"

    def _project_pauli_z(self):
        # Projection dans la base de calcul (Pauli Z)
        self.apply_gate(ZGate)
        self.normalize()
def string_rep_states(n_qubits=2):
    state_strs = ['{:02b}'.format(i) for i in range(2 ** n_qubits)]
    return state_strs


def plt_measure_qubit(out_register_qubit):
    try:
        out_register_qubit._project_pauli_z()
        probabilities = np.abs(out_register_qubit._array) ** 2
        out_register = out_register_qubit._array
        n_qubits = int(np.log2(out_register.shape[0]))
        fig, ax = plt.subplots(1, 1)

        x_values = np.array(list(range(2 ** n_qubits)))
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


def plt_measure_two_qubits(out_register_qubit1, out_register_qubit2):
    try:
        out_register_qubit1._project_pauli_z()
        out_register_qubit2._project_pauli_z()
        # Concaténer les deux qubits pour obtenir l'état conjoint
        concatenated_state = np.kron(out_register_qubit1._array, out_register_qubit2._array)

        # Calculer les probabilités
        probabilities = np.abs(concatenated_state) ** 2

        prob1 = probabilities[1]
        probabilities[1] = probabilities[2]
        probabilities[2] = prob1
        # Créer un graphique
        n_qubits = 2
        fig, ax = plt.subplots(1, 1)

        x_values = np.array(list(range(2 ** n_qubits)))
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


def plt_mesure_n_qubit(*out_register_qubits):
    try:
        for qubit in out_register_qubits:
            qubit._project_pauli_z()
        # Concaténer les états de tous les qubits pour obtenir l'état conjoint
        concatenated_state = reduce(np.kron, [qubit._array for qubit in out_register_qubits])

        # Calculer les probabilités
        probabilities = np.abs(concatenated_state) ** 2

        # Créer un graphique
        n_qubits = len(out_register_qubits)
        fig, ax = plt.subplots(1, 1)

        x_values = np.array(list(range(2 ** n_qubits)))
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

