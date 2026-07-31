# tests/conftest.py
"""Shared pytest fixtures for the whole test suite."""

import pytest

from deep_foundation_bearing_capacity.constants.constants import PSI2PSF
from deep_foundation_bearing_capacity.cross_sections.cross_sections import CircularSection, SquareSection
from deep_foundation_bearing_capacity.geomaterials.layer import Layer
from deep_foundation_bearing_capacity.geomaterials.rock import Rock
from deep_foundation_bearing_capacity.geomaterials.soil import Soil


# ---------- Soil fixtures (typical instances) ----------
@pytest.fixture
def mixed_soil():
    """
    Mixed soil: c > 0, phi > 0.
    
    Guaranteed properties (tests may depend on these):
    ALL
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
    """
    Cohesive soil (clay): c > 0, phi = 0.
    
    Guaranteed properties (tests may depend on these):
    ALL
    """
 
    return Soil(
        soil_index=1,
        unit_weight=120.0,
        friction_angle=0.0,
        cohesion=2000.0,       # psf
        n60=15
    )


@pytest.fixture
def soft_clay():
    """
    Guaranteed properties (tests may depend on these):
    ALL
    """
    
    return Soil(
        soil_index=2,
        unit_weight=100.0,
        friction_angle=0.0,
        cohesion=500.0,
        n60=4
    )


@pytest.fixture
def loose_sand():
    """
    Cohesionless soil (sand): c = 0, phi > 0.
    
    Guaranteed properties (tests may depend on these):
    ALL
    """
    return Soil(
        soil_index=3,
        unit_weight=110.0,
        friction_angle=28.0,
        cohesion=0.0,
        n60=8
    )


@pytest.fixture
def dense_sand():
    """
    Guaranteed properties (tests may depend on these):
    ALL
    """
    return Soil(
        soil_index=4,
        unit_weight=130.0,
        friction_angle=40.0,
        cohesion=0.0,
        n60=45
    )


@pytest.fixture
def igm_cohesionless():
    """
    Cohesionless IGM: sand with special advanced type.
    
    Guaranteed properties (tests may depend on these):
    ALL
    """
 
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

# ---------- Rock fixtures (typical instances) ----------
@pytest.fixture
def competent_rock():
    """
    Guaranteed properties (tests may depend on these):
    ALL
    """
    return Rock(rock_index = 0, unit_weight = 150, elastic_modulus = 5000 * PSI2PSF,
                 friction_angle = 30, qu = 5e6 * PSI2PSF, rqd = 100, 
                 rock_type = "A", rock_quality = "Very good", 
                 rock_type_advanced = None, 
                 joint = "closed")

@pytest.fixture
def igm_cohesive():
    """
    Guaranteed properties (tests may depend on these):
    ALL
    """
    return Rock(rock_index = 0, unit_weight = 135, elastic_modulus = 1000 * PSI2PSF,
                 friction_angle = 27, qu = 1e4, rqd = 50, 
                 rock_type = "B", rock_quality = "Fair", 
                 rock_type_advanced = "igm_cohesive", 
                 joint = "closed")

@pytest.fixture
def layer_typical_1(stiff_clay):
    """
    A typical layer with clay
    """
    return Layer(layer_index = 0, geomaterial = stiff_clay, ground_water_depth  = 0,
                 top_depth = 0, thickness = 10)

@pytest.fixture
def layer_typical_2(loose_sand):
    """
    A typical layer with sand
    """
    return Layer(layer_index = 1, geomaterial = loose_sand, ground_water_depth  = 0,
                 top_depth = 10, thickness = 10)

@pytest.fixture
def layer_typical_3(competent_rock):
    """
    A typical layer with compent rock
    """
    return Layer(layer_index = 2, geomaterial = competent_rock, ground_water_depth  = 0,
                 top_depth = 20, thickness = 10)

@pytest.fixture
def dict_layer(stiff_clay):
    return {"layer_index": 0,
            "geomaterial": stiff_clay,
            "ground_water_depth": 0,
            "top_depth": 0,
            "thickness": 10
            }

@pytest.fixture
def circular_section_typical():
    """
    typical circular section
    """
    return CircularSection(section_dimension = 1)

@pytest.fixture
def square_section_typical():
    """
    typical square section
    """
    return SquareSection(section_dimension = 1)