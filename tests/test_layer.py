# test /geomaterial/layer.py
from deep_foundation_bearing_capacity.geomaterials.layer import Layer


# =================================
# 1. Test construction
# =================================
class TestConstruction:
    def test_clay_layer_construction(self, layer_typical_1, stiff_clay):
        """
        Test clay layer construction
        """
        assert layer_typical_1.layer_index == 0
        assert layer_typical_1.geomaterial == stiff_clay
        assert layer_typical_1.ground_water_depth == 0
        assert layer_typical_1.top_depth == 0
        assert layer_typical_1.thickness == 10

    def test_sand_layer_construction(self, layer_typical_2, loose_sand):
        """
        Test sand layer construction
        """
        assert layer_typical_2.layer_index == 1
        assert layer_typical_2.geomaterial == loose_sand
        assert layer_typical_2.ground_water_depth == 0
        assert layer_typical_2.top_depth == 10
        assert layer_typical_2.thickness == 10

    def test_rock_layer_construction(self, layer_typical_3, competent_rock):
        """
        Test rock layer construction
        """
        assert layer_typical_3.layer_index == 2
        assert layer_typical_3.geomaterial == competent_rock

