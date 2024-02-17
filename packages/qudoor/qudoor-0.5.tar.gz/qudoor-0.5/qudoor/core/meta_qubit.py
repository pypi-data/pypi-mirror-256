# myquantumlib/core/meta_qubit.py
import numpy as np
from matplotlib import pyplot as plt

from qudoor.core.constants import I


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
        self._array = np.dot(gate_matrix, self._array)

    def apply_state(self, state):
        self.state = state
        self._array = np.array(state, dtype=np.complex128)  # Assurez-vous que le vecteur d'état est de type complexe
        norm = np.linalg.norm(self._array)
        if norm != 0:
            self._array /= norm  # Normalisation du vecteur d'état
        self.apply_gate(I)
        return self

    def mesure(self):
        out_register = self._array
        n_qubits = int(np.log2(out_register.shape[0]))
        max = 0
        # Assurez-vous que la longueur des probabilités est correcte
        probabilities = basis_state_probs(out_register)
        xray = string_rep_states(n_qubits)
        prob = {}
        for i, j in zip(probabilities, xray):
            try:
                for k in i:
                    prob[j] = k
            except:
                prob[j] = i

        for var in prob:
            if prob[var] > max:
                max = prob[var]

        result = ""
        for cle in prob.keys():
            if prob[cle] == max:
                result = cle
                break
        return result

def basis_state_probs(svec):
    norm = np.linalg.norm(svec)
    return np.abs(svec) ** 2 / norm ** 2 if norm != 0 else np.abs(svec) ** 2

def string_rep_states(n_qubits=3):
    state_strs = ['' for _ in range(2 ** n_qubits)]
    basis_strs = ['0', '1']

    for q in range(n_qubits):
        for i in range(len(state_strs)):
            b = basis_strs[(i // (2 ** q)) % 2]
            state_strs[i] = state_strs[i] + b

    return state_strs


def plt_measure(out_register_qubit):
    try:
        out_register = out_register_qubit._array
        n_qubits = int(np.log2(out_register.shape[0]))
        fig, ax = plt.subplots(1, 1)

        x_values = np.array(list(range(2 ** n_qubits)))

        ax.bar(x_values, basis_state_probs(out_register))
        ax.set_xticks(x_values)
        ax.set_xticklabels(string_rep_states(n_qubits))
        ax.set_ylim(0, 1)
        ax.grid(True)
        ax.set_ylabel(r'$P(S_c)$')
        ax.set_xlabel(r'$S_c$')
        plt.show()
    except:
        raise TypeError("Impossible with a size if size is not a multiple of 4 or if size is 2")










