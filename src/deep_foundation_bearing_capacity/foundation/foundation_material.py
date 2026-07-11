# classes for foundation materials
from abc import abstractmethod

import numpy as np

from deep_foundation_bearing_capacity.constants.constants import (
    ELASTIC_MODULUS_CONCRETE,
    PSI2PSF,
    SCALAR_TYPE,
    YIELD_STRENGTH_CONCRETE,
)


class FoundationMaterial:
    '''
    Class for foundation material
    '''
    def __init__(self, unit_weight: float, elastic_modulus: float = None):
        '''
        Args:
            unit_weight (float): foundation material unit weight in unit of pcf
            elastic modulus (float): elastic modulus in unit of psf
        '''

        self._sanity_check_unit_weight(unit_weight)
        self._sanity_check_elastic_modulus(elastic_modulus)

        self.unit_weight = unit_weight
        self.elastic_modulus = elastic_modulus

    
    def _sanity_check_unit_weight(self, unit_weight:float)->bool:
        '''
        To perform sanity check on unit_weight
        '''
        if unit_weight <= 0:
            raise ValueError("ERROR: unit_weight shall be a positive value.")
        

        return True
    

    
    def _sanity_check_elastic_modulus(self, elastic_modulus: float) -> bool:
        if elastic_modulus <= 0:
            raise ValueError("ERROR: elastic_modulus shall be a positive value.")

class FoundationConcrete(FoundationMaterial):
    def __init__(self, unit_weight:float = 150, elastic_modulus:float = ELASTIC_MODULUS_CONCRETE, 
                 yield_strength: float = YIELD_STRENGTH_CONCRETE):
        super().__init__(unit_weight, elastic_modulus)

        self._sanity_check_elastic_modulus(elastic_modulus)
        self._sanity_check_yield_strength(yield_strength)

        # concrete yield strength in unit of psf
        self.yield_strength = yield_strength

    def _sanity_check_elastic_modulus(self, elastic_modulus:float)->bool:
        '''
        Args:
            elastic_modulus (float): concrete elastic modulus in unit of psf
        '''
        elastic_modulus_lower_bound_percentage = 0.7
        elastic_modulus_upper_bound_percentage = 10.0
        

        if elastic_modulus < (elastic_modulus_lower_bound_percentage * ELASTIC_MODULUS_CONCRETE) or ( 
           elastic_modulus > (elastic_modulus_upper_bound_percentage * ELASTIC_MODULUS_CONCRETE)):
            raise ValueError("ERROR: concrete elastic_modulus is out of normal range.")
        
        return True
    
    def _sanity_check_yield_strength(self, yield_strength:float)->bool:
        '''
        Sanity check on yield strength
        Args:
            yield_strength (float): concrete yield strength
        '''
        yield_strength_lower_bound_percentage = 0.7
        yield_strength_upper_bound_percentage = 5.0
        yield_strength_typical = 4000.0 * PSI2PSF

        if yield_strength < yield_strength_lower_bound_percentage * yield_strength_typical or (
            yield_strength > yield_strength_upper_bound_percentage * yield_strength_typical):
            raise ValueError("ERROR: concrete yield_strength is out of normal range.")

        return True
