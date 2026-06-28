# classes for segments

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.cross_sections.cross_sections import CrossSection
from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import FactorOfSafetyDeepFoundation
from deep_foundation_bearing_capacity.segments.unit_resistance import EndResistance, SideResistance
from deep_foundation_bearing_capacity.soil_layer.layer import Layer


class Segment:
    '''
    Segment accounts for not only cross section and section_length, 
    but also layer and side resistance and end bearing
    One segment corresponds to only one layer.
    
    '''
    def __init__(self, cross_section: CrossSection, layer: Layer,
                 fs:FactorOfSafetyDeepFoundation = None):

        # segment length is layer's thickness
        self.segment_length = layer.thickness

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


        
    @property
    def _side_surface_area(self):
        '''
        # calculate side surface area
        
        '''
        return self.cross_section._perimeter * self.segment_length
        
        
    def _side_resistance(self, fs: FactorOfSafetyDeepFoundation = None):
        '''
        To calculate side resistance
        
        
        '''

        side_resistance_unit = SideResistance(self.layer).side_resistance_unit()
        side_resistance = side_resistance_unit * self._side_surface_area

        # Apply factor of safety when needed
        if not fs is None:
            side_resistance = side_resistance / fs.fs_deep_foundation_skin

        return side_resistance
        
    def _end_resistance(self, fs: FactorOfSafetyDeepFoundation = None):
        '''
        To calculate end resistance.
        '''

        end_resistance_unit = EndResistance(self.layer).end_resistance_unit()
        end_resistance = end_resistance_unit * self.cross_section._cross_section_area

        if not fs is None:
            end_resistance = end_resistance / fs.fs_deep_foundation_end

        return end_resistance
    