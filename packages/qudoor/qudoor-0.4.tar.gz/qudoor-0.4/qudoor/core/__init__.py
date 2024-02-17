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
        c = np.array([self._array[0], self._array[1], other._array[0], other._array[1]])
        return np.dot(c, CX)

    def concatenate(self, other):
        self._array = np.concatenate([self._array, other._array])

