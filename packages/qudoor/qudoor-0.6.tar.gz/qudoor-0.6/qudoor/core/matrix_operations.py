import ctypes
import numpy as np

# Charge la bibliothèque partagée C
matrix_ops = ctypes.CDLL('C:\\Users\\moham\\PycharmProjects\\newhash\\qudoor\\core\\matrix_operations.dll',
                         mode=ctypes.RTLD_GLOBAL)

# Définit la signature de la fonction
matrix_ops.matrix_multiply.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
                                       ctypes.POINTER(ctypes.c_double), ctypes.c_int]


def matrix_multiply_c(matrix_a, matrix_b):
    try:
        size = matrix_a.shape[0]
        result = np.empty((size, size), dtype=np.float64)
        matrix_ops.matrix_multiply(matrix_a.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                                   matrix_b.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                                   result.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                                   ctypes.c_int(size))
        return result
    except:
        raise "Error shape of matrix"
