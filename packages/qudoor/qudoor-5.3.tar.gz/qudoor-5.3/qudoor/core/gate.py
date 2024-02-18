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

    def apply(self, control_index, target_index):
        control_array = self.qubits[control_index]._array
        target_array = self.qubits[target_index]._array

        result = cnot_array(control_array, target_array)
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