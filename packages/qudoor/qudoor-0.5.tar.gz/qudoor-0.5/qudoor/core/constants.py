import numpy as np
from scipy.linalg import block_diag

I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
CX = block_diag(np.eye(2), np.flip(np.eye(2)))


def inverse(matrix):
    return np.linalg.inv(matrix)


def swap_gate():
    return np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]])


SW = swap_gate()
T_gate = np.array([[1, 0],
                   [0, np.exp(complex(0, np.pi / 4.))]])


def build_gate_mat(gates):
    gmat = np.array([1])
    for g in gates:
        gmat = np.kron(gmat, g)
    return gmat
