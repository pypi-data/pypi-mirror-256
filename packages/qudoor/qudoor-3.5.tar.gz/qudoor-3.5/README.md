This module is Qudoor, its a module for qubit opperation using numpy, scipy and ctypes for a simulation of qubit with bit:

        qubit0 = qudoor.Qubit([0, 0])
        # apply hazmare matrix in the qubit
        qubit0.apply_gate(qudoor.H)
        print(qubit0.mesure())