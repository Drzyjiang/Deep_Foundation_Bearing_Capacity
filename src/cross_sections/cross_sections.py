# Deep foundation classes

from abc import ABC

import numpy as np

from src.constants import constants


class CrossSection:
    '''
    Class for general cross section
    '''
    def __init__(self, section_length: constants.SCALAR_TYPE):
        '''
        Args:
            section_length (constants.SCALAR_TYPE): length in unit of ft for current section
        
        '''

        # sanity check on section_length
        self._sanity_check_section_dimension(section_length)

        self.section_length = section_length

        @ABC
        def calculate_area(self):
            pass


    def _sanity_check_section_dimension(self, section_length)->bool:
        '''
        Args:
            section_length (constants.SCALAR_TYPE): length in unit of ft for current section
        '''

        if isinstance(section_length, constants.SCALAR_TYPES):
            return True
        else:
            raise TypeError(f"ERROR: section_length shall be type {constants.SCALAR_TYPES}")

class CircularSection(CrossSection):
    '''
    Class for circular cross-section
    '''
    def __init__(self, section_dimension):
        super.__init__(self, section_dimension)

        # 
        self._sanity_check_section_dimension(section_dimension)
        self.diameter = section_dimension
        self.area = self.calculate_area()

    def calculate_area(self):
        '''
        To calculate area of the cross-section
        '''

        return 0.25* np.pi *self.diameter*self.diameter

class SquareSection(CrossSection):
    '''
    Class for square cross-section
    '''
    def __init__(self, section_dimension):
        super.__init__(self, )

        # 
        self._sanity_check_section_dimension(section_dimension)
        self.diameter = section_dimension
        self.area = self.calculate_area()

    def calculate_area(self):
        '''
        To calculate area of the cross-section
        '''

        return self.diameter*self.diameter

