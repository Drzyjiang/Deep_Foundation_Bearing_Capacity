# classes for segments

from constants import constants
from cross_sections.cross_sections import CrossSection
from segments.unit_resistance import SideResistance


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