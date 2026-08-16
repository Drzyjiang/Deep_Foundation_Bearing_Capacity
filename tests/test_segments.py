# test segments/segments
import numpy as np
import pytest

from deep_foundation_bearing_capacity.constants.constants import UNIT_WEIGHT_CONCRETE, UNIT_WEIGHT_WATER


# =======================
# 1. test construction
# =======================
class TestConstruction:
    def test_construction(self, segment_typical_1, circular_section_typical, layer_typical_1,
                          foundation_concrete_typical):
        """
        Test construction
        """
        assert segment_typical_1.segment_length == layer_typical_1.thickness
        assert segment_typical_1.cross_section == circular_section_typical
        assert segment_typical_1.layer == layer_typical_1
        assert segment_typical_1.foundation_material == foundation_concrete_typical

# =======================
# 2. test properties
# =======================
EPSILON = 1E-6
class TestProperties:
    def test_side_surface_area(self, segment_typical_1, segment_typical_2):
        """
        Test side_surface_area()
        """
        assert segment_typical_1.side_surface_area == segment_typical_1.segment_length * (
                                                    segment_typical_1.cross_section.perimeter)
        assert segment_typical_2.side_surface_area == segment_typical_2.segment_length * (
                                                    segment_typical_2.cross_section.perimeter)


    def test_self_weight_total(self, segment_typical_1, segment_typical_2):
        """
        Test self_weight_total()
        """
        assert segment_typical_1.self_weight_total == pytest.approx(
            150.0 * 10 * np.pi *1*1/4.0, rel = EPSILON)

        assert segment_typical_2.self_weight_total == pytest.approx(
            150.0 * 10 * 1*1, rel = EPSILON)

    #@pytest.mark.parametrize("ground_water_depth_new", [0, 10, 20])
    def test_self_weight_effective(self, segment_typical_1, segment_typical_2):
        """
        Test self_weight_effective()
        """
        assert segment_typical_1.self_weight_effective == segment_typical_1.cross_section.area * (
            UNIT_WEIGHT_CONCRETE * segment_typical_1.segment_length  -
            UNIT_WEIGHT_WATER * segment_typical_1.segment_length)
