import numpy as np
from qudoor.core.meta_qubit import MetaQubit


def initialyse_qubit(state):
    _cr = load_dict_for_state(state)
    return _cr, np.array(state, dtype=np.float64)


def load_dict_for_state(state):
    etaqubit = MetaQubit().apply_state(state)
    metaqubit = {f"qubit": etaqubit, "mesure": etaqubit.mesure()}
    return metaqubit
