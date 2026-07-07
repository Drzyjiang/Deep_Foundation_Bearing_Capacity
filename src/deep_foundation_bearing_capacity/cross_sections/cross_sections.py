# Deep foundation classes

from abc import ABC, abstractmethod

import numpy as np

#from soil_layer.layer import Layer
from deep_foundation_bearing_capacity.constants import constants


class CrossSection(ABC):
    '''
    Class for general cross section
    '''
    def __init__(self, section_dimension):
        '''

        '''
        self._sanity_check_section_dimension(section_dimension)

        self.section_dimension = section_dimension

    def _sanity_check_section_dimension(self,section_dimension):
        '''
        Sanity check on section_dimension
        '''

        if not isinstance(section_dimension, constants.SCALAR_TYPES):
            raise TypeError(f"ERROR: section_dimension shall be {constants.SCALAR_TYPES}")
        elif section_dimension <= 0:
            raise ValueError(f"ERROR: section_dimension shall be greater than zero.")
        else:
            return True

    # calculate cross-section area
    @property
    @abstractmethod
    def cross_section_area(self):
        ...
    
    # calculate perimeter
    @property
    @abstractmethod
    def perimeter(self):
        ...


class CircularSection(CrossSection):
    '''
    Class for circular cross-section
    '''
    def __init__(self, section_dimension):
        super().__init__(section_dimension)

        # 
        self.diameter = section_dimension


    @property
    def cross_section_area(self):
        '''
        To calculate area of the cross-section
        '''

        return 0.25* np.pi *self.diameter*self.diameter
    
    @property
    def perimeter(self):
        '''
        To calculate perimeter of cross section
        '''
        return np.pi *  self.diameter
    

class SquareSection(CrossSection):
    '''
    Class for square cross-section
    '''
    def __init__(self, section_dimension):
        super().__init__(section_dimension)

        # 

        self.length = section_dimension

    @property
    def cross_section_area(self):
        '''
        To calculate area of the cross-section
        '''

        return self.length*self.length

    @property
    def perimeter(self):
        '''
        To calculate perimeter of cross section
        '''
        return  4 * self.length