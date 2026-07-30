# test /geomaterial/layer.py
import numpy as np
import pytest

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


# =================================
# 2. Test sanity checks
# =================================

class TestSanityChecks:
    @pytest.mark.parametrize("thickness", [-10, -0.1])
    def test_sanity_check_thickness(self, thickness):
        """
        Test sanity check on thickness
        """
        with pytest.raises(ValueError, match = "thickness"):
            Layer(layer_index=0, thickness = thickness)

# =================================
# 3. Test from_dict classmethod
# =================================
class TestFromDict:
    def test_from_dict_basic(self, dict_layer, stiff_clay):
        """
        Test construction by dict
        """
        layer = Layer.from_dict(dict_layer)
        assert layer.layer_index == 0
        assert layer.ground_water_depth == 0
        assert layer.geomaterial == stiff_clay
        assert layer.top_depth == 0
        assert layer.thickness == 10


# =================================
# 4. test numpy array input
# =================================
@pytest.mark.parametrize("layer_index", [np.array([0]), np.array(-1)])
@pytest.mark.parametrize("ground_water_depth", [np.array([10])])
@pytest.mark.parametrize("top_depth", [np.array([-1]), np.array(10)])
@pytest.mark.parametrize("thickness", [np.array([10])])
class TestNumpyInput:
    def test_numpy_input(self, layer_index, ground_water_depth, top_depth, thickness):
        """
        Test using numpy array as input
        """
        layer = Layer(layer_index = layer_index,
                      ground_water_depth = ground_water_depth,
                      top_depth = top_depth,
                      thickness = thickness)
        assert layer.layer_index == layer_index.item(0)
        assert layer.ground_water_depth == ground_water_depth.item(0)
        assert layer.top_depth == top_depth.item(0)
        assert layer.thickness == thickness.item(0)

# =================================
# 5. test output
# =================================
class TestDisplayProperties:
    def test_display_properties(self, layer_typical_1, capsys):
        """
        Test display_properties() method
        """
        layer_typical_1.display_properties()

        captured = capsys.readouterr()
        assert "layer_index" in captured.out
        assert "ground_water_depth" in captured.out
        assert "top_depth" in captured.out
        assert "thickness" in captured.out
