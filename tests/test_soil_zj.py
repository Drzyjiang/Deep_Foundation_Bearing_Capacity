# test /geomaterials/soil.py
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

    def test_igm_advanced_type(self, cohesionless_igm):
        assert cohesionless_igm.soil_type_advanced == "igm_cohesionless"

# =========================================================
# 2. test sanity check
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
# 5. test modify method
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

    def test_modify_soil_type_advanced(self, cohesionless_igm):
        """
        Test modifying soil_type_advanced
        """
        cohesionless_igm.modify_soil_type_advanced( "gs")
        assert cohesionless_igm.soil_type_advanced == "gs" 