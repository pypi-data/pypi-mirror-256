import numpy as np
from matplotlib import pyplot as plt

from qudoor.core.meta_qubit import *
from qudoor.core.constants import *
from qudoor.core.matrix_operations import *
from qudoor.core.QubitArray import *


class Qubit(MetaQubit):
    def __init__(self, state: list):
        super().__init__(state)
        self._initialyse_qubit(self.state)

    def change_state(self, state):
        self.state = state
        self._array = np.array(state)

    def _initialyse_qubit(self, state):
        qubit = initialyse_qubit(state)
        self._array = qubit[1]
        return qubit[0]

    def apply_cnot(self, other):
        # Contract 2nd index of CNOT_tensor with control index, and 3rd index of CNOT_tensor with target index.
        self._array = np.tensordot(CX, self._array, ((2, 3), (other._array[0], other._array[0])))
        # Put axes back in the right place
        self._array = np.moveaxis(self._array, (0, 1), (other._array[0], other._array[0]))

    def concatenate(self, other):
        self._array = np.kron(self._array, other._array)

