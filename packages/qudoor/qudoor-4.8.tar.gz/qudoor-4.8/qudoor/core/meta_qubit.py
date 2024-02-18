# myquantumlib/core/meta_qubit.py
import random
import warnings
from ast import literal_eval

import numpy as np
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
        self.apply_gate(H)
        if norm != 0:
            self._array = self._array / norm
        else:
            # Si la norme est 0, cela signifie que le qubit est dans l'état |0⟩
            self._array = np.array([1, 0], dtype=np.complex128)

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
        combined_state = np.kron(other._array, self._array)

        # Porte CNOT
        gate = matrix
        new_state = np.dot(combined_state, gate)
        # Extraire la matrice de l'état du qubit cible
        _, new_array = np.split(new_state, 2, axis=0)
        self._array = new_array

    def apply_gate_three_gubit(self, other1, other2, matrix):
        combined_state = np.kron(np.kron(self._array, other1._array), other2._array)
        gate = matrix
        new_state = np.dot(combined_state, gate)

        new_array_content, _2 = np.split(new_state, 2, axis=0)
        new_array, _ = np.split(new_array_content, 2, axis=0)
        self._array = new_array

    def mesure_qubit(self):
        try:
            # Vérifier si le vecteur d'état est correctement normalisé
            norm = np.linalg.norm(self._array)
            if not np.isclose(norm, 1.0):
                raise ValueError(f"Le vecteur d'état n'est pas correctement normalisé. Norme actuelle : {norm}")

            # Calculer les probabilités de mesure
            probabilities = np.abs(self._array.flatten()) ** 2

            # Effectuer la mesure stochastique
            result = np.random.choice([0, 1], p=probabilities)

            # Mettre à jour le vecteur d'état après la mesure
            new_state = np.zeros_like(self._array, dtype=complex128)
            new_state[result] = 1
            self._array = new_state / np.sqrt(np.sum(np.abs(new_state) ** 2))

            return f"{result} $ with the qubit Array:{str(self._array)}"
        except ValueError as e:
            print(f"Erreur lors de la mesure : {e}")
            exit(1)

def string_rep_states(n_qubits=2):
    state_strs = ['{:02b}'.format(i) for i in range(2 ** n_qubits)]
    return state_strs


def plt_measure_qubit(out_register_qubit):
    try:
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
def plt_measure_two_qubits(out_register_qubit1, out_register_qubit2):
    try:
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

