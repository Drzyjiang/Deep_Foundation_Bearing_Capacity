# classes for segments

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.cross_sections.cross_sections import CrossSection
from deep_foundation_bearing_capacity.segments.unit_resistance import SideResistance


class Segment:
    '''
    Segment accounts for not only cross section and section_length, 
    but also layer and side resistance and end bearing
    
    '''
    def __init__(self, cross_section: CrossSection, section_length: constants.SCALAR_TYPE, layer):

        # sanity check on section_length
        self._sanity_check_section_dimension(section_length)
        self.section_length = section_length

        # cross section type
        self.cross_section = cross_section

        # layer
        self.layer = layer


 

        # side resistance
        #self.side_resistance = _calculate_side_resistance()

    def _sanity_check_section_dimension(self, section_length)->bool:
        '''
        Args:
            section_length (constants.SCALAR_TYPE): length in unit of ft for current section
        '''

        if isinstance(section_length, constants.SCALAR_TYPES):
            return True
        else:
            raise TypeError(f"ERROR: section_length shall be type {constants.SCALAR_TYPES}")
        
    @property
    def _side_surface_area(self):
        '''
        # calculate side surface area
        
        '''
        return self.cross_section._cross_section_area * self.section_length
        
        
    def  _side_resistance(self):
        '''
        To calculate side resistance
        
        
        '''

        side_resistance_unit = SideResistance(self.layer).side_resistance_unit()
        #side_resistance = side_resistance_unit * 
        