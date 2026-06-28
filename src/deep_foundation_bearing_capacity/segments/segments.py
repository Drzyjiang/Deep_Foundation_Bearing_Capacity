# classes for segments

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.cross_sections.cross_sections import CrossSection
from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import FactorOfSafetyDeepFoundation
from deep_foundation_bearing_capacity.segments.unit_resistance import EndResistance, SideResistance


class Segment:
    '''
    Segment accounts for not only cross section and section_length, 
    but also layer and side resistance and end bearing
    
    '''
    def __init__(self, cross_section: CrossSection, section_length: constants.SCALAR_TYPE, layer,
                 fs:FactorOfSafetyDeepFoundation = None):

        # sanity check on section_length
        self._sanity_check_section_dimension(section_length)
        self.section_length = section_length

        # cross section type
        self.cross_section = cross_section

        # layer
        self.layer = layer

        # factor of safety
        self.fs = fs

        # side resistance
        self.side_resistance = self._side_resistance(None)

        # end resistance
        self.end_resistance = self._end_resistance(None)


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
        return self.cross_section._perimeter * self.section_length
        
        
    def _side_resistance(self, fs = None):
        '''
        To calculate side resistance
        
        
        '''

        side_resistance_unit = SideResistance(self.layer).side_resistance_unit()
        side_resistance = side_resistance_unit * self._side_surface_area

        # Apply factor of safety when needed
        if not fs is None:
            side_resistance = side_resistance / self.fs.fs_deep_foundation_skin

        return side_resistance
        
    def _end_resistance(self, fs = None):
        '''
        To calculate end resistance.
        '''

        end_resistance_unit = EndResistance(self.layer).end_resistance_unit_cohesionless()
        end_resistance = end_resistance_unit * self.cross_section._cross_section_area

        return end_resistance
    