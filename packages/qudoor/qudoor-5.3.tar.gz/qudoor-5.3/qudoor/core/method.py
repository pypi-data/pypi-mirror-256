from qudoor.core.constants import *
import numpy as np
import scipy.sparse as ss

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

def apply_t(qubit):
    array = qubit._array
    newarray = apply_gate(array, T_gate)
    return meta_qubit_array(newarray)

def concatenante_qubit_array(array0, array1):
    a0a = array0[0]
    a0b = array0[1]
    a1a = array1[0]
    a1b = array1[1]
    return np.array([a0a, a0b, a1a, a1b])

def split_qubit_array(array):
    a0a = array[0]
    a0b = array[1]
    a1a = array[2]
    a1b = array[3]
    return np.array([a0a, a0b]), np.array([a1a, a1b])


def cnot_array(array1:np.ndarray, array2:np.ndarray):
    a0a = array1[0]
    a0b = array1[1]
    b0a = array2[0]
    b0b = array2[1]
    c0areal = (a0a.real + b0a.real) % 2
    c0aimag = (a0a.imag + b0a.imag) % 2
    c0a = c0areal + 1j * c0aimag
    c0breal = (a0b.real + b0b.real) % 2
    c0bimag = (a0b.imag + b0b.imag) % 2
    c0b = c0breal + 1j * c0bimag
    return np.array([c0a, c0b])