import numpy as np
from scipy.linalg import block_diag
complex128 = np.complex128

I = np.array([[1, 0],
                    [0, 1]], dtype=complex128)
X = np.array([[0, 1],
                    [1, 0]], dtype=complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex128)
Z = np.array([[1, 0], [0, -1]], dtype=complex128)
H = 1 / np.sqrt(2) * np.array([[1, 1],
                               [1, -1]], dtype=complex128)
S = np.array([[1, 0],
              [0, 1j]])

P = np.array([
    [1, 0],
    [0, 1j]
], dtype=complex128)

CCX_matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 1, 0]], dtype=np.complex128)

raX = (1 / 2) * np.array(
    [
        [1 + 1j, 1 - 1j],
        [1 - 1j, 1 + 1j]
    ], dtype=complex128
)


def rxx_matrix(phi):
    return np.array([
        [np.cos(phi), 0, 0, -1j * np.sin(phi)],
        [0, np.cos(phi), -1j * np.sin(phi), 0],
        [0, -1j * np.sin(phi), np.cos(phi), 0],
        [-1j * np.sin(phi), 0, 0, np.cos(phi)]
    ], dtype=complex128)

def U2(phi, lamba):
    return 1/np.sqrt(2) * np.array([
        [1, -1*np.exp(1j*lamba)],
        [np.exp(1j*phi), np.exp(1j*(phi + lamba))]
    ], dtype=complex128)

def U1(lamba):
    return U(0, 0, lamba)

def U(theta, phi, lamba):
    return 1 / np.sqrt(2) * np.array([
        [np.cos(theta/2), -1 * np.exp(1j * lamba)*np.sin(theta/2)],
        [np.exp(1j * phi)*np.sin(theta/2), np.exp(1j * (phi + lamba))*np.cos(theta/2)]
    ], dtype=complex128)

def ryy_matrix(phi):
    return np.array([
        [np.cos(phi), 0, 0, 1j * np.sin(phi)],
        [0, np.cos(phi), -1j * np.sin(phi), 0],
        [0, -1j * np.sin(phi), np.cos(phi), 0],
        [1j * np.sin(phi), 0, 0, np.cos(phi)]
    ], dtype=complex128)


def rx_matrix(a):
    return np.array([
        [np.cos(a / 2), -1j * np.sin(a / 2)],
        [-1j * np.sin(a / 2), np.cos(a / 2)]
    ], dtype=complex128)


def ry_matrix(a):
    return np.array([
        [np.cos(a / 2), -1 * np.sin(a / 2)],
        [-1 * np.sin(a / 2), np.cos(a / 2)]
    ], dtype=complex128)


def rz_matrix(a):
    return np.array([
        [np.exp(-1j * a / 2), 0],
        [0, np.exp(1j * a / 2)]
    ], dtype=complex128)


def r_matrix(phi):
    return np.array([
        [1, 0],
        [0, np.exp(1j * phi)]
    ], dtype=complex128)


def inverse(matrix):
    return np.linalg.inv(matrix)


def swap_gate():
    return np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1]], dtype=complex128)


SW = swap_gate()
rswp = (1 / 2) * (1 + 1j)
rswm = (1 / 2) * (1 - 1j)
raSW = np.array([
    [1, 0, 0, 0],
    [0, rswp, rswm, 0],
    [0, rswm, rswp, 0],
    [0, 0, 0, 1]
], dtype=complex128)
T_gate = np.array([[1, 0],
                   [0, np.exp(1j * np.pi / 4)]], dtype=complex128)

CNOT_matrix = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0]], dtype=complex128)


def build_gate_mat(gates):
    gmat = np.array([1])
    for g in gates:
        gmat = np.kron(gmat, g)
    return gmat
