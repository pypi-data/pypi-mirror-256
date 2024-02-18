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

def single_cnot_bit(control, target):
    if control == 1:
        return (target+1)%2
    if control == 0:
        return target
    else:
        print("error")
        exit(1)

def bit_to_array(bit0):
    if bit0 == 0:
        return np.array([1, 0])
    else:
        return np.array([0, 1])


def cnot_control_bit_target_array(control, target):
    if control == 0:
        return target
    else:
        newarray = apply_gate(target, X)
        return newarray


def divide_matricielle_qubit(array0, array1):
    a0a = array0[0]
    a0b = array0[1]
    a0c = array0[2]
    a0d = array0[3]
    b0a = array1[0]
    b0b = array1[1]
    c0a = (a0a / b0a) + (a0b / b0a)
    c0b = (a0c / b0b) + (a0d / b0b)
    return np.array([c0a, c0b])