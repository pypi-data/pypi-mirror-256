import numpy as np
from scipy.linalg import block_diag

I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
CNOT_matrix = block_diag(np.eye(2), np.flip(np.eye(2)))
CX=np.reshape(CNOT_matrix, (2,2,2,2))
projectors=[np.array([[1,0],[0,0]]), np.array([[0,0],[0,1]]) ]
S = np.array([
    [1, 0],
    [0, 1j]
])

raX = (1 / 2) * np.array(
    [
        [1 + 1j, 1 - 1j],
        [1 - 1j, 1 + 1j]
    ]
)


def rxx_matrix(phi):
    return np.array([
        [np.cos(phi), 0, 0, -1j * np.sin(phi)],
        [0, np.cos(phi), -1j * np.sin(phi), 0],
        [0, -1j * np.sin(phi), np.cos(phi), 0],
        [-1j * np.sin(phi), 0, 0, np.cos(phi)]
    ])

def ryy_matrix(phi):
    return np.array([
        [np.cos(phi), 0, 0, 1j * np.sin(phi)],
        [0, np.cos(phi), -1j * np.sin(phi), 0],
        [0, -1j * np.sin(phi), np.cos(phi), 0],
        [1j * np.sin(phi), 0, 0, np.cos(phi)]
    ])

def rx_matrix(a):
    return np.array([
        [np.cos(a / 2), -1j * np.sin(a / 2)],
        [-1j * np.sin(a / 2), np.cos(a / 2)]
    ])


def ry_matrix(a):
    return np.array([
        [np.cos(a / 2), -1 * np.sin(a / 2)],
        [-1 * np.sin(a / 2), np.cos(a / 2)]
    ])


def rz_matrix(a):
    return np.array([
        [np.exp(-1j * a / 2), 0],
        [0, np.exp(1j * a / 2)]
    ])


def r_matrix(phi):
    return np.array([
        [1, 0],
        [0, np.exp(1j * phi)]
    ])


def inverse(matrix):
    return np.linalg.inv(matrix)


def swap_gate():
    return np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]])


SW = swap_gate()
rswp = (1 / 2) * (1 + 1j)
rswm = (1 / 2) * (1 - 1j)
raSW = np.array([
    [1, 0, 0, 0],
    [0, rswp, rswm, 0],
    [0, rswm, rswp, 0],
    [0, 0, 0, 1]
])
T_gate = np.array([[1, 0],
                   [0, np.exp(1j*np.pi / 4)]])


def build_gate_mat(gates):
    gmat = np.array([1])
    for g in gates:
        gmat = np.kron(gmat, g)
    return gmat
