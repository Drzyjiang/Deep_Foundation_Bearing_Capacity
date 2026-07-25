# tests/conftest.py
"""Shared pytest fixtures for the whole test suite."""

import pytest

from deep_foundation_bearing_capacity.geomaterials.soil import Soil

# ---------- Soil fixtures (typical instances) ----------

@pytest.fixture
def mixed_soil():
    """
    Mixed soil: c > 0, phi > 0.
    """
    return Soil(
        soil_index=1,
        unit_weight=120.0,
        friction_angle=27.0,
        cohesion=100.0,       # psf
        n60=15
    )

@pytest.fixture
def stiff_clay():
    """Cohesive soil (clay): c > 0, phi = 0."""
    return Soil(
        soil_index=1,
        unit_weight=120.0,
        friction_angle=0.0,
        cohesion=2000.0,       # psf
        n60=15
    )


@pytest.fixture
def soft_clay():
    return Soil(
        soil_index=2,
        unit_weight=100.0,
        friction_angle=0.0,
        cohesion=500.0,
        n60=4
    )


@pytest.fixture
def loose_sand():
    """Cohesionless soil (sand): c = 0, phi > 0."""
    return Soil(
        soil_index=3,
        unit_weight=110.0,
        friction_angle=28.0,
        cohesion=0.0,
        n60=8
    )


@pytest.fixture
def dense_sand():
    return Soil(
        soil_index=4,
        unit_weight=130.0,
        friction_angle=40.0,
        cohesion=0.0,
        n60=45
    )


@pytest.fixture
def igm_cohesionless():
    """Cohesionless IGM: sand with special advanced type."""
    return Soil(
        soil_index=5,
        unit_weight=135.0,
        friction_angle=42.0,
        cohesion=0.0,
        n60=60,
        soil_type_advanced="igm_cohesionless"
    )

@pytest.fixture
def dict_basic():
    """
    dictionary basic for initialization
    """
    return {
            "soil_index": 0, 
            "unit_weight": 120, 
            "friction_angle": 30,
            "cohesion": 100, 
            "n60": 30,
            "soil_type_advanced": None
        }

@pytest.fixture
def dict_igm():
    """
    dictionary for igm
    """
    return {
            "soil_index": 0, 
            "unit_weight": 120, 
            "friction_angle": 30,
            "cohesion": 100, 
            "n60": 30,
            "soil_type_advanced": "igm_cohesionless"
            }

@pytest.fixture
def dict_gs():
    """
    dictionary for gs
    """
    return {
            "soil_index": 0, 
            "unit_weight": 120, 
            "friction_angle": 30,
            "cohesion": 100, 
            "n60": 30,
            "soil_type_advanced": "gs"
            }