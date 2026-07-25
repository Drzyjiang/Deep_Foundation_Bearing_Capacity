# Classes for geomaterials

from abc import ABC, abstractmethod

import numpy as np

from deep_foundation_bearing_capacity.constants import constants


class Geomaterial:
    def __init__(self, unit_weight:float = 0, elastic_modulus: float = 0):
        '''
        Args:
            unit_weight (float): unit weight in unit of pound per cubic foot
            elastic_modulus (float): elastic modulus in unit of psf
        '''

        self._sanity_check_unit_weight(unit_weight)
        
        # TODO
        # self._sanity_check_elastic_modulus(elastic_modulus)

        self.unit_weight = unit_weight
        self.elastic_modulus = elastic_modulus
        


    def _sanity_check_unit_weight(self, unit_weight):
        '''
        To perform sanity check on unit weight
        '''

        if not isinstance(unit_weight, constants.NUMERIC_TYPES):
            raise TypeError("unit_weight data type shall be float, int, np.ndarray, np.generic.")
        
        # sanity check on soil unit weight

        if np.min(np.asarray(unit_weight)) < constants.UNIT_WEIGHT_WATER:
            raise ValueError("ERROR: soil unit_weight is unlikely smaller than water unit weight.")

        return True    
    
    # TODO
    def _sanity_check_elastic_modulus(elastic_modulus):
        '''
        To perform sanity check on elastic modulus
        '''
        pass

    def modify_unit_weight(self, unit_weight_new):
        '''
        To modify self.unit_weight.
        '''

        self._sanity_check_unit_weight(unit_weight_new)

        self.unit_weight = unit_weight_new

    @abstractmethod
    def display_properties(self, properties:list[str]):
        '''
        To display specified geomaterial properties

        Args:
            properties (list[str]): strs that match geomaterial properties in that class
        '''
        pass