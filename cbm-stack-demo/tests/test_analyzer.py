# tests/test_analyzer.py

import numpy as np
import pytest

from cbm_engine.analyzer import compute_rms, compute_fft, detect_threshold


def test_compute_rms():
    signal = [0, 1, -1, 1, -1]
    expected_rms = np.sqrt(np.mean(np.array(signal) ** 2))
    assert np.isclose(compute_rms(signal), expected_rms)


def test_compute_fft():
    signal = [1, 0, -1, 0]
    spectrum = compute_fft(signal)
    assert len(spectrum) == len(signal)
    # Le module de la FFT doit être positif
    assert all(s >= 0 for s in spectrum)


def test_detect_threshold():
    assert detect_threshold(5, threshold=3) is True
    assert detect_threshold(2, threshold=3) is False
    assert detect_threshold(3, threshold=3) is True


if __name__ == "__main__":
    pytest.main()
# Run the tests when this file is executed directly
