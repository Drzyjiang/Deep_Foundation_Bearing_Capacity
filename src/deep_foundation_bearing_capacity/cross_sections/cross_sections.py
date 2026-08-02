# Deep foundation classes

from abc import ABC, abstractmethod

import numpy as np

#from soil_layer.layer import Layer
from deep_foundation_bearing_capacity.constants.constants import NUMERIC_TYPE


class CrossSection(ABC):
    '''
    Class for general cross section
    '''
    CROSS_SECTION_NAME = "UNDEFINED"

    def __init__(self, section_dimension):
        '''

        '''
        self._sanity_check_section_dimension(section_dimension)

        self.section_dimension = section_dimension

    def _sanity_check_section_dimension(self,section_dimension: NUMERIC_TYPE):
        '''
        Sanity check on section_dimension
        '''

        if not isinstance(section_dimension, NUMERIC_TYPE):
            raise TypeError(f"ERROR: section_dimension shall be {NUMERIC_TYPE}")
        elif section_dimension <= 0:
            raise ValueError(f"ERROR: section_dimension shall be greater than zero.")
        else:
            return True
   

    # calculate cross-section area
    @property
    @abstractmethod
    def area(self):
        ...
    
    # calculate perimeter
    @property
    @abstractmethod
    def perimeter(self):
        ...

    @abstractmethod
    def display_properties(self):
        """
        Display cross-section properties
        """
        pass


class CircularSection(CrossSection):
    '''
    Class for circular cross-section
    '''
    CROSS_SECTION_NAME = "Circular Section"


    def __init__(self, section_dimension):
        super().__init__(section_dimension)

        self.diameter = section_dimension


    @property
    def area(self):
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

    def display_properties(self, properties: list[str] = ["CROSS_SECTION_NAME", "diameter", 
                                                          "perimeter", "area"]):
        """
        Display properties
        """
        #sanity check
        for property in properties:
            try: 
                print(f"{property} is: {getattr(self, property)}")
            except AttributeError:
                print(f"ERROR: {property} does not exist.")

class SquareSection(CrossSection):
    '''
    Class for square cross-section
    '''
    CROSS_SECTION_NAME = "Square Section"

    def __init__(self, section_dimension):
        super().__init__(section_dimension)

        # 

        self.length = section_dimension

    @property
    def area(self):
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

    def display_properties(self, properties: list[str] = ["CROSS_SECTION_NAME", "length", 
                                                          "perimeter", "area"]):
        """
        Display properties
        """
        #sanity check
        for property in properties:
            try: 
                print(f"{property} is: {getattr(self, property)}")
            except AttributeError:
                print(f"ERROR: {property} does not exist.")