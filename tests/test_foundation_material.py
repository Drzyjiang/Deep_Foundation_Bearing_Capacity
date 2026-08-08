# test foundation/foundation_material.py
import pytest

from deep_foundation_bearing_capacity.constants.constants import ELASTIC_MODULUS_CONCRETE, YIELD_STRENGTH_CONCRETE
from deep_foundation_bearing_capacity.foundation.foundation_material import FoundationConcrete

# ====================
# 1. Test Construction
# ====================
EPSILON = 1e-6
class TestConstruction:
    def test_foundation_concrete(self, foundation_concrete_typical):
        """
        Test foundation concrete
        """
        assert foundation_concrete_typical.unit_weight == pytest.approx(150.0, rel = EPSILON)
        assert foundation_concrete_typical.elastic_modulus == pytest.approx(ELASTIC_MODULUS_CONCRETE, rel = EPSILON)
        assert foundation_concrete_typical.yield_strength == pytest.approx(YIELD_STRENGTH_CONCRETE, rel = EPSILON)

# ====================
# 2. Test SanityChecks
# ====================
class TestSanityChecks:
    def test_sanity_check_unit_weight(self):
        """
        Sanity check on unit weigth
        """
        with pytest.raises(ValueError, match ="unit_weight"):
            FoundationConcrete(unit_weight = -1)


    def test_sanity_check_elastic_modulus(self, foundation_concrete_typical):
        """
        Sanity check on elastic modulus
        """
        elastic_modulus_too_low = (foundation_concrete_typical.elastic_modulus_lower_bound_percentage-0.01) *(
                                    ELASTIC_MODULUS_CONCRETE)
        with pytest.raises(ValueError, match = "elastic_modulus"):
            FoundationConcrete(elastic_modulus = elastic_modulus_too_low)

        elastic_modulus_too_high = (foundation_concrete_typical.elastic_modulus_upper_bound_percentage+0.01) *(
                                    ELASTIC_MODULUS_CONCRETE)

        with pytest.raises(ValueError, match = "elastic_modulus"):
            FoundationConcrete(elastic_modulus = elastic_modulus_too_high)

    def test_sanity_check_yield_strength(self, foundation_concrete_typical):
        """
        Sanity check on yield strength
        """
        yield_strength_too_low = (foundation_concrete_typical.yield_strength_lower_bound_percentage-0.01) *(
                                    YIELD_STRENGTH_CONCRETE)
        yield_strength_too_high = (foundation_concrete_typical.yield_strength_upper_bound_percentage+0.01) *(
                                    YIELD_STRENGTH_CONCRETE)

        with pytest.raises(ValueError, match = "yield_strength"):
            FoundationConcrete(yield_strength = yield_strength_too_low)

        with pytest.raises(ValueError, match = "yield_strength"):
            FoundationConcrete(yield_strength = yield_strength_too_high)