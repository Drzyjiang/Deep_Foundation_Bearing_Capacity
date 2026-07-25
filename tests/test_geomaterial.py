# test /geomaterials/geomaterial
import pytest

from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial


@pytest.fixture
def geomaterial():
    return Geomaterial(unit_weight=120, elastic_modulus=1000000)

# =========================================================
# 1. Test construction
# =========================================================
class TestGeomaterialConstruction:
    def test_construction(self, geomaterial):
        assert geomaterial.unit_weight == 120
        assert geomaterial.elastic_modulus == 1000000

# =========================================================
# 2. Test sanity checks
# =========================================================
class TestSanityChecks:
    @pytest.mark.parametrize("unit_weight", [-1, 0, 62.3])
    def test_sanity_check_unit_weight(self, unit_weight):
        """
        Test sanity check on unit weight
        """
        with pytest.raises(ValueError, match="unit_weight"):
            Geomaterial(unit_weight = unit_weight)

# =========================================================
# 3. Test modify methods
# =========================================================
class TestModifyMethods:
    @pytest.mark.parametrize("unit_weight_new", [100,120])
    def test_modify_unit_weight(self, unit_weight_new, geomaterial):
        """
        Test modify_unit_weight
        """
        geomaterial.modify_unit_weight(unit_weight_new)
        assert geomaterial.unit_weight == unit_weight_new

    @pytest.mark.parametrize("unit_weight_new_invalid", [-1, 0])
    def test_modify_unit_weight_invalid(self, unit_weight_new_invalid, geomaterial):
        """
        Test modify_unit_weight with invalid input values
        """
        with pytest.raises(ValueError, match = "unit_weight"):
            geomaterial.modify_unit_weight(unit_weight_new_invalid)

