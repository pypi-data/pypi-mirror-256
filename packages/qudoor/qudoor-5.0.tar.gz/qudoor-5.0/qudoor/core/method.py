from qudoor.core.constants import *
import numpy as np

class MtArray:
    def __init__(self, array):
        self._array = array

def apply_gate(array, gate):
    return np.dot(gate, array)

def meta_qubit_array(array):
    qb = MtArray(array)
    return qb

def inverse_qubit(qubit):
    array = qubit._array
    newarray = apply_gate(array, X)
    return meta_qubit_array(newarray)

def apply_hadamar(qubit):
    array = qubit._array
    newarray = apply_gate(array, H)
    return meta_qubit_array(newarray)

def controle_qubit(qubit):
    array = apply_gate(qubit._array, Z)
    array = normalize(array)
    prob = np.abs(array) ** 2
    result = np.random.choice([False, True], p=prob)
    return result

def control_n_qubit(qubits):
    probs = []
    for i in qubits:
        probs.append(controle_qubit(i))

    prob = False
    prbint = 0
    for j in probs:
        if j:
            prbint += 1
    if len(probs) == prbint:
        prob = True

    return prob

def retTrue():
    return True

def apply_y(qubit):
    array = qubit._array
    newarray = apply_gate(array, Y)
    return meta_qubit_array(newarray)

def apply_z(qubit):
    array = qubit._array
    newarray = apply_gate(array, Z)
    return meta_qubit_array(newarray)

def apply_raX(qubit):
    array = qubit._array
    newarray = apply_gate(array, raX)
    return meta_qubit_array(newarray)

def apply_ph(qubit):
    array = qubit._array
    newarray = apply_gate(array, P)
    return meta_qubit_array(newarray)

controllers = [control_n_qubit]


def normalize(array):
    norm = np.linalg.norm(array)
    if norm != 0:
        array = array / norm
    return array

def apply_i(qubit):
    array = qubit._array
    newarray = apply_gate(array, I)
    return meta_qubit_array(newarray)