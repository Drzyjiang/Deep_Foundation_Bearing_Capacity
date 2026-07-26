# test /geomaterials/soil.py
import numpy as np
import pytest

from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial
from deep_foundation_bearing_capacity.geomaterials.soil import Soil


# =========================================================
# 1. Test construction
# =========================================================
class TestSoilConstruction:
    def test_clay_construction(self, stiff_clay): 
        assert stiff_clay.soil_index == 1
        assert stiff_clay.unit_weight == 120.0
        assert stiff_clay.friction_angle == 0.0
        assert stiff_clay.cohesion == 2000.0 # psf
        assert stiff_clay.n60 == 15

    def test_sand_construction(self, loose_sand):
        assert loose_sand.soil_index == 3
        assert loose_sand.unit_weight == 110.0
        assert loose_sand.friction_angle == 28.0
        assert loose_sand.cohesion == 0.0
        assert loose_sand.n60 == 8

    def test_default_soil_type_advanced_is_none(self, stiff_clay):
        assert stiff_clay.soil_type_advanced == None

    def test_igm_advanced_type(self, igm_cohesionless):
        assert igm_cohesionless.soil_type_advanced == "igm_cohesionless"

# =========================================================
# 2. test sanity checks
# =========================================================

class TestSanityChecks:
    @pytest.mark.parametrize("bad_friction_angle", [-1.0, -10.0])
    def  test_sanity_check_friction_angle(self, bad_friction_angle):
        with pytest.raises(ValueError, match = "friction_angle"):
            Soil(soil_index = 0, friction_angle = bad_friction_angle)


    @pytest.mark.parametrize("bad_cohesion", [-1, -1000])
    def test_sanity_check_cohesion(self, bad_cohesion):
        with pytest.raises(ValueError, match = "cohesion"):
            Soil(soil_index = 1, cohesion = bad_cohesion)

    @pytest.mark.parametrize(["bad_friction_angle", "bad_cohesion"], [(0, 0)])
    def test_sanity_check_friction_angle_cohesion(self, bad_friction_angle, bad_cohesion):
        with pytest.raises(ValueError, match = "friction_angle and cohesion"):
            Soil(soil_index = 2, friction_angle = bad_friction_angle, cohesion = bad_cohesion)

    @pytest.mark.parametrize("bad_n60", [-1, -100])
    def test_sanity_check_n60(self, bad_n60):
        with pytest.raises(ValueError, match = "n60"):
            Soil(soil_index = 3, friction_angle = 1, cohesion = 1, n60 = bad_n60)

# =========================================================
# 3. from_dict classmethod
# =========================================================
class TestFromDict:
    def test_from_dict_basic(self, dict_basic):
        """
        Test initialization by dict_basic
        """
        soil = Soil.from_dict(dict_basic)

        assert soil.soil_index == 0
        assert soil.unit_weight == 120
        assert soil.friction_angle == 30
        assert soil.cohesion == 100
        assert soil.n60 == 30
        assert soil.soil_type_advanced == None

    def test_from_dict_igm(self, dict_igm):
        """
        Test initizalization by dict_igm
        """
        soil = Soil.from_dict(dict_igm)
        assert soil.soil_type_advanced == "igm_cohesionless"

    def test_from_dict_gs(self, dict_gs):
        """
        Test initizalization by dict_gs
        """
        soil = Soil.from_dict(dict_gs)
        assert soil.soil_type_advanced == "gs"


# =========================================================
# 4. test soil_type_genernal
# =========================================================
class TestSoilTypeGeneral:
    def test_mix_is_0(self, mixed_soil):
        """
        When friction_angle != 0 and cohesion != 0, return 0
        """
        assert mixed_soil.soil_type_general == 0

    def test_sand_is_1(self, dense_sand):
        """
        sand should have soil_type_general == 1
        """
        assert dense_sand.soil_type_general == 1

    def test_clay_is_2(self, stiff_clay):
        """
        clay should have soil_type_general == 2
        """
        assert stiff_clay.soil_type_general == 2

# =========================================================
# 5. test modify methods
# =========================================================
class TestModifyMethods:
    @pytest.mark.parametrize("friction_angle_new", [0, 10,20,30])
    def test_modify_friction_angle(self, friction_angle_new, stiff_clay, mixed_soil, loose_sand):
        """
        Test modifying friction angle
        """
        stiff_clay.modify_friction_angle(friction_angle_new)
        assert stiff_clay.friction_angle == friction_angle_new

        mixed_soil.modify_friction_angle(friction_angle_new)
        assert mixed_soil.friction_angle == friction_angle_new

        # friction_angle and cohesion cannot be zero simultaneously
        if friction_angle_new == 0:
            with pytest.raises(ValueError, match = "friction_angle and cohesion"):
                loose_sand.modify_friction_angle(friction_angle_new)
        else:
            loose_sand.modify_friction_angle(friction_angle_new)
            assert loose_sand.friction_angle == friction_angle_new

    @pytest.mark.parametrize("friction_angle_new_invalid", [-1, -100])
    def test_modify_friction_angle_invalid(self, friction_angle_new_invalid, stiff_clay, mixed_soil, 
                                           loose_sand, igm_cohesionless):
        """
        Test modifying friction angle with invalid values
        """
        with pytest.raises(ValueError, match = "friction_angle"):
            stiff_clay.modify_friction_angle(friction_angle_new_invalid)

        with pytest.raises(ValueError, match = "friction_angle"):
            mixed_soil.modify_friction_angle(friction_angle_new_invalid)

        with pytest.raises(ValueError, match = "friction_angle"):
            loose_sand.modify_friction_angle(friction_angle_new_invalid)

        with pytest.raises(ValueError, match = "friction_angle"):
            igm_cohesionless.modify_friction_angle(friction_angle_new_invalid)
        
            
    @pytest.mark.parametrize("cohesion_new", [0, 1000,10000])
    def test_modify_cohesion(self, cohesion_new, stiff_clay, mixed_soil, dense_sand):
        """
        Test modify cohesion method
        """
        if cohesion_new == 0:
            with pytest.raises(ValueError, match = "friction_angle and cohesion"):
                stiff_clay.modify_cohesion(cohesion_new)
        else:
            stiff_clay.modify_cohesion(cohesion_new)
            assert stiff_clay.cohesion == cohesion_new

        mixed_soil.modify_cohesion(cohesion_new)
        assert mixed_soil.cohesion == cohesion_new

        dense_sand.modify_cohesion(cohesion_new)
        assert dense_sand.cohesion == cohesion_new

    @pytest.mark.parametrize("cohesion_new_invalid", [-1, -1000])
    def test_modify_cohesion_invalid(self, cohesion_new_invalid, stiff_clay, mixed_soil, 
                                           loose_sand, igm_cohesionless):
        """
        Test modifying cohesion with invalid values
        """
        with pytest.raises(ValueError, match = "cohesion"):
            stiff_clay.modify_cohesion(cohesion_new_invalid)

        with pytest.raises(ValueError, match = "cohesion"):
            mixed_soil.modify_cohesion(cohesion_new_invalid)

        with pytest.raises(ValueError, match = "cohesion"):
            loose_sand.modify_cohesion(cohesion_new_invalid)

        with pytest.raises(ValueError, match = "cohesion"):
            igm_cohesionless.modify_cohesion(cohesion_new_invalid)

    def test_modify_soil_type_advanced(self, igm_cohesionless):
        """
        Test modifying soil_type_advanced
        """
        igm_cohesionless.modify_soil_type_advanced( "gs")
        assert igm_cohesionless.soil_type_advanced == "gs" 

        igm_cohesionless.modify_soil_type_advanced( "igm_cohesionless")
        assert igm_cohesionless.soil_type_advanced == "igm_cohesionless" 

# =========================================================
# 6. test numpy array input
# =========================================================
class TestNumpyInput:
    @pytest.mark.parametrize("soil_index", [np.array([0])])
    @pytest.mark.parametrize("friction_angle", [np.array([30]), np.array([0])])
    @pytest.mark.parametrize("cohesion", [np.array([100])])
    @pytest.mark.parametrize("n60", [np.array([10])])
    def test_numpy_friction_angle(self, soil_index, friction_angle, cohesion,
                                  n60):
        """
        Test using friction angle in format of np.ndarray
        """
        soil = Soil(soil_index = soil_index, friction_angle = friction_angle, cohesion = cohesion,
                     n60 = n60)
        assert soil.soil_index == soil_index.item(0)
        assert soil.friction_angle == friction_angle.item(0)
        assert soil.cohesion == cohesion.item(0)
        assert soil.n60 == n60.item(0)

# =========================================================
# 7. test output methods
# =========================================================
class TestDisplayProperties:
    """
    Test display_properties() method
    """
    def test_display_properties(self, capsys, soft_clay):
        soft_clay.display_properties()
        captured = capsys.readouterr()
        assert "soil_index" in captured.out
        assert "unit_weight" in captured.out
        assert "friction_angle" in captured.out
        assert "cohesion" in captured.out
        assert "n60" in captured.out

# =========================================================
# 7. test inheritance
# =========================================================
class TestInheritance:
    def test_is_geomaterial(self, stiff_clay, igm_cohesionless):
        from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial
        assert isinstance(stiff_clay, Geomaterial)
        assert isinstance(igm_cohesionless, Geomaterial)