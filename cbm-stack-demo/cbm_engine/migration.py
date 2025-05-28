# cbm_engine/migration.py

import numpy as np


def migrated_rms(signal):
    """
    Calcule le RMS (Root Mean Square) d'un signal,
    en imitant le comportement d'une fonction MATLAB typique.

    signal : list[float] ou np.ndarray
    return : float
    """
    signal_array = np.array(signal)
    return np.sqrt(np.mean(signal_array ** 2))
