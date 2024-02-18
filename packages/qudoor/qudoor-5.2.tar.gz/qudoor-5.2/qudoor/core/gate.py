import warnings

import numpy as np

from qudoor.core.method import *

class Gate:
    def __init__(self, qubit_num, qubit_control_num, method_if_control, method_control, qubits):
        self.method = method_if_control
        self.qubit_num = qubit_num
        self.qubit_control_num = qubit_control_num
        self.controller = method_control
        self.qubits = qubits
    
    def control(self, control_index):
        if self.qubit_control_num > 0:
            result_control = self.controller(self.qubits[control_index])
            return result_control
        else:
            return True

    def controls(self, controls_index):
        quntrol = []
        for i in controls_index:
            quntrol.append(self.qubits[i])

        result_control = self.controller(quntrol)
        return result_control

    def apply_method(self, target_index):
        result_method = self.method(self.qubits[target_index])
        self.qubits[target_index] = result_method
    
    def apply_if_control(self, controller_result, target_index):
        if controller_result:
            self.qubits[target_index] = self.method(self.qubits[target_index])
    
    def apply(self, control_or_controls_index, target_index):
        if self.controller in controllers:
            result_control = self.controls(control_or_controls_index)
        else:
            result_control = self.control(control_or_controls_index)
        self.apply_if_control(result_control, target_index)

    def retQbit(self, index):
        return self.qubits[index]
        
class XGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, inverse_qubit, retTrue, qubits)
        
        
class CXGate(Gate):
    def __init__(self, qubits):
        super().__init__(2, 1, inverse_qubit, controle_qubit, qubits)

    def apply(self, control_or_controls_index, target_index):
        qcarray = self.qubits[control_or_controls_index]._array
        qtarray = self.qubits[target_index]._array
        if qtarray[0] != 0 and qtarray[0] != 1 and qtarray[1] != 0 and qtarray[1] != 1:
            if qcarray[0] != 0 and qcarray[0] != 1 and qcarray[1] != 0 and qcarray[1] != 1:
                b0a = qcarray[0] / np.sqrt(2)
                b0b = qcarray[1] / np.sqrt(2)
                b0acnot = cnot_control_bit_target_array(0, qtarray) * b0a
                b0bcnot = cnot_control_bit_target_array(1, qtarray) * b0b
                result = (1 / np.sqrt(2)) * divide_matricielle_qubit(np.array([b0acnot[0], b0acnot[1], b0bcnot[0], b0bcnot[1]]), qcarray)
            else:
                probqc = np.abs(qcarray) ** 2
                bitt2 = np.random.choice([0, 1], p=probqc)
                result = cnot_control_bit_target_array(bitt2, qtarray)

            self.qubits[target_index] = MtArray(result)

        else:
            probs = np.abs(qtarray) ** 2
            bitt = np.random.choice([0, 1], p=probs)
            if qcarray[0] != 0 and qcarray[0] != 1 and qcarray[1] != 0 and qcarray[1] != 1:
                b0a = qcarray[0] / np.sqrt(2)
                b0b = qcarray[1] / np.sqrt(2)
                b0acnot = single_cnot_bit(0, bitt) * b0a
                b0bcnot = single_cnot_bit(1, bitt) * b0b
                result = (1/np.sqrt(2)) * np.array([b0acnot, b0bcnot])
            else:
                probqc = np.abs(qcarray) ** 2
                bitt2 = np.random.choice([0, 1], p=probqc)
                result = bit_to_array(single_cnot_bit(bitt2, bitt))

            self.qubits[target_index] = MtArray(result)


class CXXGate(Gate):
    def __init__(self, qubits):
        super().__init__(3, 2, inverse_qubit, control_n_qubit, qubits)


class YGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_y, retTrue, qubits)


class ZGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_z, retTrue, qubits)

class PGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_ph, retTrue, qubits)

class RaXGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_raX, retTrue, qubits)

class HGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_hadamar, retTrue, qubits)

class IGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_i, retTrue, qubits)

class TGate(Gate):
    def __init__(self, qubits):
        super().__init__(1, 0, apply_t, retTrue, qubits)