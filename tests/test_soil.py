# tests/test_soil.py
"""Tests for Soil class."""

import numpy as np
import pytest

from deep_foundation_bearing_capacity.geomaterials.soil import Soil

# =========================================================
# 1. Construction: valid inputs
# =========================================================

class TestSoilConstruction:
    """Construction should succeed with valid inputs and store attributes correctly."""

    def test_clay_construction(self, stiff_clay):
        assert stiff_clay.soil_index == 1
        assert stiff_clay.unit_weight == 120.0
        assert stiff_clay.friction_angle == 0.0
        assert stiff_clay.cohesion == 2000.0
        assert stiff_clay.n60 == 15

    def test_sand_construction(self, dense_sand):
        assert dense_sand.friction_angle == 40.0
        assert dense_sand.cohesion == 0.0

    def test_default_soil_type_advanced_is_none(self, stiff_clay):
        assert stiff_clay.soil_type_advanced is None

    def test_igm_advanced_type(self, cohesionless_igm):
        assert cohesionless_igm.soil_type_advanced == "igm_cohesionless"


# =========================================================
# 2. Sanity checks: invalid inputs should raise
# =========================================================

class TestSoilSanityChecks:
    """Invalid inputs must raise proper errors early (fail fast)."""

    # ---- unit_weight ----
    @pytest.mark.parametrize("bad_uw", [-1.0, 0.0, 50.0])   # < water = 62.4
    def test_unit_weight_below_water_raises(self, bad_uw):
        with pytest.raises(ValueError, match="unit weight"):
            Soil(soil_index=1, unit_weight=bad_uw,
                 friction_angle=30, cohesion=0, n60=10)

    def test_unit_weight_wrong_type_raises(self):
        with pytest.raises(TypeError):
            Soil(soil_index=1, unit_weight="heavy",
                 friction_angle=30, cohesion=0, n60=10)

    # ---- friction_angle ----
    @pytest.mark.parametrize("bad_phi", [-1.0, -0.001])
    def test_negative_friction_angle_raises(self, bad_phi):
        with pytest.raises(ValueError, match="friction angle"):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle=bad_phi, cohesion=1000, n60=10)

    def test_friction_angle_wrong_type_raises(self):
        with pytest.raises(TypeError):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle="thirty", cohesion=0, n60=10)

    # ---- cohesion ----
    @pytest.mark.parametrize("bad_c", [-1.0, -100.0])
    def test_negative_cohesion_raises(self, bad_c):
        with pytest.raises(ValueError, match="cohesion"):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle=30, cohesion=bad_c, n60=10)

    # ---- n60 ----
    @pytest.mark.parametrize("bad_n", [-2, -5])
    def test_negative_n60_raises(self, bad_n):
        with pytest.raises(ValueError, match="n60"):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle=30, cohesion=0, n60=bad_n)

    # ---- soil_type_advanced ----
    def test_invalid_advanced_type_raises(self):
        with pytest.raises(ValueError, match="soil_type_advanced"):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle=30, cohesion=0, n60=10,
                 soil_type_advanced="mystery_material")

    def test_advanced_type_wrong_type_raises(self):
        with pytest.raises(TypeError):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle=30, cohesion=0, n60=10,
                 soil_type_advanced=42)  # int, not str


# =========================================================
# 3. Soil type determination logic
# =========================================================

class TestSoilTypeGeneral:
    """_determine_soil_type() logic:
       Type 0: mixed (c != 0 AND phi != 0)
       Type 1: cohesionless (c == 0)
       Type 2: cohesive (c != 0, phi == 0)
    """

    def test_clay_is_type_2(self, stiff_clay):
        assert stiff_clay.soil_type_general == 2

    def test_sand_is_type_1(self, loose_sand):
        assert loose_sand.soil_type_general == 1

    def test_mixed_is_type_0(self):
        mixed = Soil(soil_index=1, unit_weight=120,
                     friction_angle=25, cohesion=500, n60=10)
        assert mixed.soil_type_general == 0

    def test_both_zero_edge_case(self):
        """Docstring says type -1 for both zero, but current code returns type 2.
        This test documents current behavior — update if the code is fixed."""
        edge = Soil(soil_index=1, unit_weight=120,
                    friction_angle=0, cohesion=0, n60=10)
        # Current implementation returns type 2 (cohesive branch when c==0 hits
        # `elif self.cohesion == 0` returns 1... actually returns 1). Trace:
        #   friction=0, cohesion=0 → first `if` False → `elif cohesion==0` True → 1
        assert edge.soil_type_general == 1  # ← 但注释说应该是 -1！


# =========================================================
# 4. from_dict classmethod
# =========================================================

class TestFromDict:

    def test_from_dict_basic(self):
        data = {
            "soil_index": 1,
            "unit_weight": 120.0,
            "friction_angle": 30.0,
            "cohesion": 500.0,
            "n60": 10,
            "soil_type_advanced": None,
        }
        soil = Soil.from_dict(data)
        assert soil.soil_index == 1
        assert soil.unit_weight == 120.0
        assert soil.friction_angle == 30.0
        assert soil.cohesion == 500.0

    def test_from_dict_string_numbers(self):
        """Values as strings should still work (from_dict does float())."""
        data = {
            "soil_index": "1",
            "unit_weight": "120.0",
            "friction_angle": "30.0",
            "cohesion": "500.0",
            "n60": 10,
            "soil_type_advanced": None,
        }
        soil = Soil.from_dict(data)
        assert soil.unit_weight == 120.0

    def test_from_dict_igm(self):
        data = {
            "soil_index": 5, "unit_weight": 135.0,
            "friction_angle": 42.0, "cohesion": 0.0, "n60": 60,
            "soil_type_advanced": "igm_cohesionless",
        }
        soil = Soil.from_dict(data)
        assert soil.soil_type_advanced == "igm_cohesionless"


# =========================================================
# 5. Modify_* methods
# =========================================================

class TestModifyMethods:

    def test_modify_unit_weight(self, stiff_clay):
        stiff_clay.modify_unit_weight(115.0)
        assert stiff_clay.unit_weight == 115.0

    def test_modify_unit_weight_invalid_raises(self, stiff_clay):
        with pytest.raises(ValueError):
            stiff_clay.modify_unit_weight(30.0)     # < water
        # State should NOT change after failed modification
        assert stiff_clay.unit_weight == 120.0

    def test_modify_friction_angle(self, dense_sand):
        dense_sand.modify_friction_angle(38.0)
        assert dense_sand.friction_angle == 38.0

    def test_modify_friction_angle_invalid_raises(self, dense_sand):
        with pytest.raises(ValueError):
            dense_sand.modify_friction_angle(-5.0)
        assert dense_sand.friction_angle == 40.0    # unchanged

    def test_modify_cohesion(self, stiff_clay):
        stiff_clay.modify_cohesion(1500.0)
        assert stiff_clay.cohesion == 1500.0

    def test_modify_cohesion_invalid_raises(self, stiff_clay):
        with pytest.raises(ValueError):
            stiff_clay.modify_cohesion(-10.0)
        assert stiff_clay.cohesion == 2000.0


# =========================================================
# 6. NumPy array inputs (since NUMERIC_TYPES includes ndarray)
# =========================================================

class TestNumpyInputs:
    """Class advertises support for numpy arrays via NUMERIC_TYPES."""

    def test_scalar_ndarray_unit_weight(self):
        soil = Soil(soil_index=1,
                    unit_weight=np.float64(120.0),
                    friction_angle=30, cohesion=0, n60=10)
        assert soil.unit_weight == 120.0

    def test_negative_in_array_raises(self):
        """Sanity check uses np.min — arrays with any negative should fail."""
        with pytest.raises(ValueError):
            Soil(soil_index=1, unit_weight=120,
                 friction_angle=np.array([30.0, -5.0, 25.0]),
                 cohesion=0, n60=10)


# =========================================================
# 7. Inheritance
# =========================================================

class TestGeomaterialInheritance:

    def test_is_geomaterial(self, stiff_clay):
        from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial
        assert isinstance(stiff_clay, Geomaterial)


# =========================================================
# 8. display_properties (smoke test)
# =========================================================

class TestDisplayProperties:

    def test_display_default(self, stiff_clay, capsys):
        stiff_clay.display_properties()
        captured = capsys.readouterr()
        assert "unit_weight" in captured.out
        assert "cohesion" in captured.out

    def test_display_custom_subset(self, stiff_clay, capsys):
        stiff_clay.display_properties(["cohesion"])
        captured = capsys.readouterr()
        assert "cohesion" in captured.out
        assert "unit_weight" not in captured.out

    def test_display_unknown_property_raises(self, stiff_clay):
        with pytest.raises(AttributeError):
            stiff_clay.display_properties(["mystery_property"])


# =========================================================
# 9. Known-issue / regression tests (currently expected to fail)
# =========================================================

class TestKnownIssues:
    """Tests documenting bugs / inconsistencies you may want to fix.
    Marked xfail so they don't break CI but are visible."""

    @pytest.mark.xfail(reason="n60 default -1 conflicts with sanity check >= 0")
    def test_default_n60_should_not_raise(self):
        """Constructor with default n60 should either accept or be documented as required."""
        Soil(soil_index=1, unit_weight=120, friction_angle=30, cohesion=0)

    @pytest.mark.xfail(reason="typo: 'elsatic_modulus' instead of 'elastic_modulus'")
    def test_elastic_modulus_attribute_name(self, stiff_clay):
        assert hasattr(stiff_clay, "elastic_modulus")
        assert not hasattr(stiff_clay, "elsatic_modulus")

    @pytest.mark.xfail(reason="Docstring says both-zero returns type -1, code returns 1")
    def test_both_zero_should_be_type_minus_1(self):
        edge = Soil(soil_index=1, unit_weight=120,
                    friction_angle=0, cohesion=0, n60=10)
        assert edge.soil_type_general == -1
