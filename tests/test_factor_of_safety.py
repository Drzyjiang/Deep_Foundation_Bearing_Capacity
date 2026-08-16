# Test factor_of_safety.factor_of_safety.py
import numpy as np
import pytest

from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import (
    FactorOfSafety,
    FactorOfSafetyDeepFoundation,
)

# =====================
# 1. Test FactorOfSafety
# =====================

class TestFactorOfSafety:
    def test_construction(self):
        """
        Test construction of class FactorOfSafety
        """
        fs = FactorOfSafety(3.0)
        assert fs.factor_of_safety == 3.0

    def test_sanity_check(self):
        """
        Test sanity_check
        """
        with pytest.raises(ValueError, match = "fs"):
            FactorOfSafety(0.9)


# =====================
# 2. Test FactorOfSafetyDeepFoundation
# =====================
class TestFactorOfSafetyDeepFoundation:
    def test_construction(self):
        """
        Test construction of class FactorOfSafetyDeepFoundation
        """
        fs = FactorOfSafetyDeepFoundation(factor_of_safety = 3.0, fs_end_bearing=2.5 )
        assert fs.fs_side_compression == 3.0
        assert fs.fs_side_uplift == 3.0
        assert fs.fs_end == 2.5

    @pytest.mark.parametrize("fs_side", [np.array([2.0])])
    @pytest.mark.parametrize("fs_end_bearing", [np.array([2.5])])
    def test_numpy(self, fs_side, fs_end_bearing):
        """
        Test input format of numpy
        """
        fs = FactorOfSafetyDeepFoundation(fs_side, fs_end_bearing)
        assert fs.fs_side_compression == fs_side
        assert fs.fs_end == fs_end_bearing

    def test_inheritance(self):
        """
        Test FactorOfSafetyDeepFoundation is a child of FactorOfSafety
        """
        fs = FactorOfSafetyDeepFoundation()
        assert isinstance(fs, FactorOfSafety)
