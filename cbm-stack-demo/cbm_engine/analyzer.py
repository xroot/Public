# cbm_engine/analyzer.py

import numpy as np
from scipy.fft import fft


def compute_rms(signal):
    """
    Calcule le RMS du signal.
    """
    signal_array = np.array(signal)
    return np.sqrt(np.mean(signal_array ** 2))


def compute_fft(signal):
    """
    Calcule la transformée de Fourier d’un signal.
    Retourne le module de la FFT (amplitude spectrale).
    """
    signal_array = np.array(signal)
    spectrum = fft(signal_array)
    return np.abs(spectrum)


def detect_threshold(value, threshold=1.0):
    """
    Détecte si une valeur dépasse un seuil.
    Peut être utilisé pour déclencher des alertes.
    """
    return value >= threshold

