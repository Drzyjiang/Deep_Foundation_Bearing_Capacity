# test /geomaterial/layer.py
from deep_foundation_bearing_capacity.geomaterials.layer import Layer


# =================================
# 1. Test construction
# =================================
class TestConstruction:
    def test_construction(self, typical_layer_1, stiff_clay):
        """
        Test construction
        """
        assert typical_layer_1.layer_index == 0
        assert typical_layer_1.geomaterial == stiff_clay
        assert typical_layer_1.ground_water_depth == 0
        assert typical_layer_1.top_depth == 0
        assert typical_layer_1.thickness == 10
