# test /geomaterials/rock.py
from dataclasses import dataclass

import numpy as np
import pytest

from deep_foundation_bearing_capacity.constants.constants import PSI2PSF
from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial
from deep_foundation_bearing_capacity.geomaterials.rock import Rock


# =============================================
# 1. Test construction
# =============================================
class TestRockConstruction:
    def test_competent_rock(self, competent_rock):
        """
        Test competent rock construction
        """
        assert competent_rock.unit_weight == 150
        assert competent_rock.elastic_modulus == 5000 * PSI2PSF
        assert competent_rock.friction_angle == 30
        assert competent_rock.qu == 5e6 * PSI2PSF
        assert competent_rock.rqd == 100
        assert competent_rock.rock_type == "A"
        assert competent_rock.rock_quality == "Very good"
        assert competent_rock.rock_type_advanced == None 
        assert competent_rock.joint == "closed"


# =========================================================
# 2. test sanity checks
# =========================================================
class TestSanityChecks:
    @pytest.mark.parametrize("qu", [-1,-1000.0])
    def test_qu(self, qu):
        """
        Test qu initialization value
        """
        with pytest.raises(ValueError, match = "qu"):
            Rock(rock_index = 0, qu = qu)

    @pytest.mark.parametrize("rqd", [-1,100.1])
    def test_rqd(self, rqd):
        """
        Test rqd initialization value
        """
        with pytest.raises(ValueError, match = "RQD"):
            Rock(rock_index = 0, rqd = rqd)

    @pytest.mark.parametrize("rock_type", ["F", "Excellent", "100"])
    def test_rock_type(self, rock_type):
        """
        Test rqd initialization value
        """
        with pytest.raises(ValueError, match = "rock_type"):
            Rock(rock_index = 0, rock_type = rock_type)

    @pytest.mark.parametrize("rock_quality", ["A", "100"])
    def test_rock_quality(self, rock_quality):
        """
        Test rqd initialization value
        """
        with pytest.raises(ValueError, match = "rock_quality"):
            Rock(rock_index = 0, rock_quality = rock_quality)

    @pytest.mark.parametrize("rock_type_advanced", ["A", "None"])
    def test_rock_type_advanced(self, rock_type_advanced):
        """
        Test rqd initialization value
        """
        with pytest.raises(ValueError, match = "rock_type_advanced"):
            Rock(rock_index = 0, rock_type_advanced = rock_type_advanced)


    @pytest.mark.parametrize("joint", ["opened", "None"])
    def test_joint(self, joint):
        """
        Test rqd initialization value
        """
        with pytest.raises(ValueError, match = "joint"):
            Rock(rock_index = 0, joint = joint)


# =========================================================
# 3. from_dict classmethod
# =========================================================
class TestFromDict:
    @pytest.fixture
    def dict_rock(self):
        """
        dictionary for rock
        """
        return {
                "rock_index": 0, 
                "unit_weight": 150,
                "elastic_modulus": 5000 * PSI2PSF, 
                "friction_angle": 30,
                "qu": 5e6 * PSI2PSF,
                "rqd": 100,
                "rock_type": "A", 
                "rock_quality": "Very good",
                "rock_type_advanced": None,
                "joint": "open"
            }
    
    def test_from_dict(self, dict_rock):
        """
        Test construction by dict
        """
        rock = Rock.from_dict(dict_rock)
        assert rock.rock_index == dict_rock.get("rock_index")
        assert rock.unit_weight == dict_rock.get("unit_weight")
        assert rock.elastic_modulus == dict_rock.get("elastic_modulus")
        assert rock.friction_angle == dict_rock.get("friction_angle")
        assert rock.qu == 5e6 * PSI2PSF
        assert rock.rqd == 100
        assert rock.rock_type == "A"
        assert rock.rock_quality == "Very good"
        assert rock.rock_type_advanced == None 
        assert rock.joint == "open"

# =========================================================
# 4. test numpy array input
# =========================================================
class TestNumpyInput:
    @pytest.mark.parametrize("rock_index", [np.array([0]), np.array([-1])])
    @pytest.mark.parametrize("friction_angle", [np.array([20]), np.array([30])])
    @pytest.mark.parametrize("qu", [np.array([5e3*PSI2PSF])])
    @pytest.mark.parametrize("rqd", [np.array([100]), np.array(0)])
    def test_numpy_input(self, rock_index, friction_angle, qu, rqd):
        """
        Test construction by numpy array
        """
        rock = Rock(rock_index = rock_index,
                    friction_angle = friction_angle,
                    qu = qu,
                    rqd = rqd)
        assert rock.rock_index == rock_index
        assert rock.friction_angle == friction_angle
        assert rock.qu == qu
        assert rock.rqd == rqd 

# =========================================================
# 5. test display_properties
# =========================================================
class TestDisplayProperties:
    def test_display_properties(self, competent_rock, capsys):
        """
        Test display_properties()
        """
        competent_rock.display_properties()
        captured = capsys.readouterr()
        assert "rock_type" in captured.out
        assert "rock_type" in captured.out
        assert "rock_index" in captured.out
        assert "unit_weight" in captured.out
        assert "qu" in captured.out
        assert "rock_quality" in captured.out
        assert "rock_type_advanced" in captured.out
        assert "joint" in captured.out

# =========================================================
# 6. test inheritance
# =========================================================
class TestInheritance:
    def test_is_geomaterial(self, competent_rock, igm_cohesive):
        """
        Test rock is inheritance of geomaterial
        """
        assert isinstance(competent_rock, Geomaterial)
        assert isinstance(competent_rock, Geomaterial)