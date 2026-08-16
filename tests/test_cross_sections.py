# test cross_sections.cross_sections.CircularSection
import numpy as np
import pytest

from deep_foundation_bearing_capacity.cross_sections.cross_sections import CircularSection, CrossSection, SquareSection

# =============================
# 1. test construction
# =============================
EPSILON = 1E-6
class TestConstruction:
    def test_circular_section(self, circular_section_typical):
        """
        test CircularSection
        """
        assert circular_section_typical.diameter == 1
        assert circular_section_typical.area == pytest.approx(0.25* np.pi * 1*1, rel = EPSILON)
        assert circular_section_typical.perimeter == pytest.approx(np.pi *  1, rel = EPSILON)

    def test_square_section(self, square_section_typical):
        """
        Test SquareSection
        """
        assert square_section_typical.length == pytest.approx(1.0, rel = EPSILON)
        assert square_section_typical.area == pytest.approx(1.0, rel = EPSILON)
        assert square_section_typical.perimeter == pytest.approx(4, rel = EPSILON)

# =============================
# 2. test sanity checks
# =============================
@pytest.mark.parametrize("wrong_dimension", [-1, np.array([-1])])
class TestSanityChecks:
    def test_sanity_check_section_dimension(self, wrong_dimension):
        """
        Test sanity check on section_dimension
        """
        with pytest.raises(ValueError, match = "section_dimension"):
            CircularSection(wrong_dimension)

        with pytest.raises(ValueError, match = "section_dimension"):
            SquareSection(wrong_dimension)


# =============================
# 3. test inheritance
# =============================
class TestInheritance:
    def test_inheritance(self, circular_section_typical, square_section_typical):
        """
        Test circular and square cross sections are children of CrossSection
        """
        assert isinstance(circular_section_typical, CrossSection)
        assert isinstance(square_section_typical, CrossSection)
