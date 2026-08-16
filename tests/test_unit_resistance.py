# test segments/unit_resistance.py
import numpy as np
import pytest

from deep_foundation_bearing_capacity.constants.constants import PSF2TSF, UNIT_WEIGHT_WATER
from deep_foundation_bearing_capacity.geomaterials.layer import Layer
from deep_foundation_bearing_capacity.geomaterials.soil import Soil
from deep_foundation_bearing_capacity.segments.unit_resistance import (
    SoilEndResistance,
    SoilSideResistance,
)

# ==========================
# 1. Test SideResistance class
# ==========================

class TestSoilSideResistance:
    """
    Test SoilSideResistance class
    Note: no correction is applied
    """

    def test_calculate_alpha_1(self):
        """
        Reference: FHWA Drilled Shaft Manual 2010 Page 13-18
                   when cohesion = 2395 psf, alpha shall be 0.55
        """
        clay = Soil(soil_index = 0,
                       unit_weight = 120,
                       friction_angle = 0,
                       cohesion = 2395,
                       n60 = 8)

        clay_layer = Layer(layer_index = 0,
                      geomaterial = clay, ground_water_depth = 100,
                      top_depth = 0,
                      thickness = 20)

        clay_unit_resistance = SoilSideResistance(clay_layer)

        assert clay_unit_resistance._calculate_alpha() == 0.55

    def test_calculate_beta_1(self):
        """
        Reference: SHAFT 2026 Users Manual Section 5.3
                   with N60 = 20, 25, beta should be 0.6.
                   Note that an average beta (of upper and lower interfaces) are manually calcualted
        """
        # fictious friction_angle
        sand_1 = Soil(soil_index = 0,
                    friction_angle = 30,
                    n60 = 20)
        sand_2 = Soil(soil_index = 1,
                    friction_angle = 30,
                    n60 = 25)

        sand_layer_upper = Layer(layer_index = 0, geomaterial = sand_1, ground_water_depth = 100,
                                top_depth = 32, thickness = 0.01)

        sand_layer_lower = Layer(layer_index = 1, geomaterial = sand_2, ground_water_depth = 100,
                                top_depth = 59, thickness = 0.01)

        beta_upper = SoilSideResistance(sand_layer_upper)._calculate_beta()
        beta_lower = SoilSideResistance(sand_layer_lower)._calculate_beta()

        assert (beta_upper + beta_lower) / 2.0 == pytest.approx(0.6, rel = 0.01)

    def test_calculate_beta_2(self, dense_sand):
        """
        To apply beta method, layer thickness shall be less than 30 ft
        """
        sand_layer_40 = Layer(layer_index=0, geomaterial=dense_sand, thickness = 40)

        with pytest.raises(ValueError, match = "thickness"):
            SoilSideResistance(sand_layer_40)._calculate_beta()

    def test_side_unit_resistance_cohesionless_1(self):
        """
        Reference: SHAFT 2026 Users Manual Section 5.2
        Note: benchmark's beta OF 0.8 is not derived from O'Neil 1999, more likely arbitary
        """
        sand_1 = Soil(soil_index = 0, unit_weight = 115, friction_angle = 30, n60 = 11)
        sand_2 = Soil(soil_index = 0, unit_weight = 115, friction_angle = 30, n60 = 14)
        sand_3 = Soil(soil_index = 0, unit_weight = 115, friction_angle = 30, n60 = 19)

        layer_1 = Layer(layer_index = 0, geomaterial = sand_1, ground_water_depth = 4, top_depth = 0,thickness = 4)
        layer_2 = Layer(layer_index = 1, geomaterial = sand_2, ground_water_depth = 4, top_depth = 4,thickness = 26)
        layer_3 = Layer(layer_index = 2, geomaterial = sand_3, ground_water_depth = 4, top_depth = 30, thickness = 60)

        layer_1_unit_resistance = SoilSideResistance(layer_1)
        assert layer_1_unit_resistance.side_resistance_unit_cohesionless(effective_stress = 115*2.0,
                                                                         beta_override = 0.8) ==(
                                                    pytest.approx(0.115 / PSF2TSF * 0.8, rel = 0.01))

        layer_2_unit_resistance = SoilSideResistance(layer_2)
        assert layer_2_unit_resistance.side_resistance_unit_cohesionless(
            effective_stress = 115*4.0 + (115-UNIT_WEIGHT_WATER) * 13, beta_override=0.8) == (
                pytest.approx(0.572 / PSF2TSF * 0.8, rel = 0.01))

        layer_3_unit_resistance = SoilSideResistance(layer_3)
        assert layer_3_unit_resistance.side_resistance_unit_cohesionless(effective_stress = 115*4.0
            + (115-UNIT_WEIGHT_WATER) * 41, beta_override=0.8) == (
                pytest.approx(1.308 / PSF2TSF * 0.8, rel = 0.01))

    def test_side_unit_resistance_cohesive_1(self):
        """
        Reference: SHAFT 2026 Users Manual Section 5.4.8
                   averaged side resistance shall be 1.14 tsf * 0.55
        Note: benchmark's alpha of 0.55 is arbitary
        """
        # Need to interpolate Su at 5 ft and at 33.4 ft
        xp = [0, 45]
        yp = [0.8 / PSF2TSF, 1.6 / PSF2TSF]
        clay_5ft = Soil(soil_index = 0, cohesion = np.interp(5, xp, yp))
        clay_33_4ft = Soil(soil_index = 0, cohesion = np.interp(33.4, xp, yp))

        clay_layer_5ft = Layer(layer_index = 0, geomaterial = clay_5ft, ground_water_depth = 100,
                                top_depth = 5,thickness = 0.01)
        clay_layer_33_4ft = Layer(layer_index = 0, geomaterial = clay_33_4ft,
                                  ground_water_depth = 100, top_depth = 33.4,thickness = 0.01)

        side_resistance_5ft = SoilSideResistance(clay_layer_5ft)
        side_resistance_33_4ft = SoilSideResistance(clay_layer_33_4ft)

        side_resistance_unit_cohesive = 0.5*(
            side_resistance_5ft.side_resistance_unit_cohesive(alpha_override = 0.55)
              + side_resistance_33_4ft.side_resistance_unit_cohesive(alpha_override=0.55))

        assert side_resistance_unit_cohesive == pytest.approx(1.14 / PSF2TSF * 0.55, rel = 0.01)

class TestSoilEndResistance:
    """
    Test SoilEndResistance class
    Note: no correction is applied
    """

    def test_end_resistance_unit_cohesive(self):
        """
        Test end_resistance_unit() for clay
        Reference: NCHRP 24-17 Appendix D Example 1
                   when cohesion = 3800 psf, unit end resistance shall be 9 *cohesion
        """

        clay = Soil(soil_index = 0,
                       unit_weight = 120,
                       friction_angle = 0,
                       cohesion = 1900*2,
                       n60 = 8)

        clay_layer = Layer(layer_index = 0,
                      geomaterial = clay, ground_water_depth = 100,
                      top_depth = 0,
                      thickness = 20)
        soil_end_resistance = SoilEndResistance(clay_layer)

        assert soil_end_resistance.end_resistance_unit_cohesive() == 9*(1900*2)

    def test_end_resistance_unit_cohesionless(self):
        """
        Test end_resistance_unit() for sand
        Reference: SHAFT 2026 Users Manual Section 5.3.8
                   when n60 = 25, unit end resistance shall be 0.6 * 25
        """

        sand = Soil(soil_index = 0, friction_angle = 30, n60 = 25)

        sand_layer = Layer(layer_index = 0, geomaterial = sand, ground_water_depth = 100, top_depth = 59,
                      thickness = 0.01)
        soil_end_resistance = SoilEndResistance(sand_layer)

        assert soil_end_resistance.end_resistance_unit_cohesionless() == 0.6 *25 / PSF2TSF
