# tests/test_migration.py

import numpy as np

from cbm_engine.migration import migrated_rms


def test_migrated_rms_with_list():
    signal = [1, -1, 1, -1, 1]
    expected = np.sqrt(np.mean(np.array(signal) ** 2))
    assert abs(migrated_rms(signal) - expected) < 1e-8


def test_migrated_rms_with_numpy_array():
    signal = np.array([2, 2, 2, 2])
    expected = np.sqrt(np.mean(signal ** 2))
    assert abs(migrated_rms(signal) - expected) < 1e-8


def test_migrated_rms_empty_signal():
    signal = []
    try:
        migrated_rms(signal)
        assert False, "Should raise an error on empty input"
    except Exception:
        pass


if __name__ == "__main__":
    import pytest

    pytest.main()
# Run the tests when this file is executed directly
