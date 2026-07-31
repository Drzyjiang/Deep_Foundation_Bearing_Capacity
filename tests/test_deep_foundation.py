# test foundation/deep_foundation.py
import pytest


# ============================
# 1. Test DeepFoundation
# ============================
class TestDeepFoundation:
    def test_construction(self, deep_foundation_typical, segment_typical_1, segment_typical_2,
                          segment_typical_3):
        """
        Test DeepFoundation construction
        """
        assert deep_foundation_typical.segments[0] == segment_typical_1
        assert deep_foundation_typical.segments[1] == segment_typical_2
        assert deep_foundation_typical.segments[2] == segment_typical_3

    def test_segment_mid_depths(self, deep_foundation_typical):
        """
        Test segment_mid_depths()
        """
        assert deep_foundation_typical._segment_mid_depths() == [5, 15, 25]

    def test_segment_bottom_depths(self, deep_foundation_typical):
        """
        Test segment_bottom_depths()
        """
        assert deep_foundation_typical._segment_bottom_depths() == [10, 20, 30]

    def test_segment_top_depths(self, deep_foundation_typical):
        """
        Test segment_top_depths()
        """
        assert deep_foundation_typical._segment_top_depths() == [0, 10, 20]
