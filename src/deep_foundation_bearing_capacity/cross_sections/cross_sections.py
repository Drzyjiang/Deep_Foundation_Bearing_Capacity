# Deep foundation classes

from abc import ABC

import numpy as np

#from soil_layer.layer import Layer
from deep_foundation_bearing_capacity.constants import constants


class CrossSection:
    '''
    Class for general cross section
    '''
    def __init__(self):
        '''
        Args:
            section_length (constants.SCALAR_TYPE): length in unit of ft for current section
        
        '''

        # calculate cross-section area
        @property
        @ABC
        def _calculate_cross_section_area(self):
            ...

        # calculate side surface area
        @property
        @ABC
        def _calculate_side_surface_area(self):
            ...






class CircularSection(CrossSection):
    '''
    Class for circular cross-section
    '''
    def __init__(self, section_dimension):
        super.__init__(self, section_dimension)

        # 
        self._sanity_check_section_dimension(section_dimension)
        self.diameter = section_dimension


    def _calculate_cross_section_area(self):
        '''
        To calculate area of the cross-section
        '''

        return 0.25* np.pi *self.diameter*self.diameter
    
    def _calculate_side_surface_area(self):
        '''
        To
        '''

class SquareSection(CrossSection):
    '''
    Class for square cross-section
    '''
    def __init__(self, section_dimension):
        super.__init__(self, )

        # 
        self._sanity_check_section_dimension(section_dimension)
        self.diameter = section_dimension


    def _calculate_cross_section_area(self):
        '''
        To calculate area of the cross-section
        '''

        return self.diameter*self.diameter

