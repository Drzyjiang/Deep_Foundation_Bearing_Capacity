# classes for segments

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.cross_sections.cross_sections import CrossSection
from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import FactorOfSafetyDeepFoundation
from deep_foundation_bearing_capacity.foundation.foundation_material import FoundationMaterial
from deep_foundation_bearing_capacity.segments.unit_resistance import EndResistance, SideResistance
from deep_foundation_bearing_capacity.soil_layer.layer import Layer


class Segment:
    '''
    Segment accounts for not only cross section and section_length, 
    but also layer and side resistance and end bearing
    One segment corresponds to only one layer and one cross_section.
    
    '''
    def __init__(self, cross_section: CrossSection, layer: Layer, foundation_material:FoundationMaterial = None, 
                 fs:FactorOfSafetyDeepFoundation = None):
        '''
        
        '''
        # segment length is layer's thickness
        self.segment_length = layer.thickness

        # cross section type
        self.cross_section = cross_section

        # layer
        self.layer = layer

        # factor of safety
        self.fs = fs

        self.foundation_material = foundation_material

        # initialize end_resistance
        self.end_resistance = self.calculate_end_resistance()

        
    @property
    def side_surface_area(self):
        '''
        # calculate side surface area
        
        '''
        return self.cross_section.perimeter * self.segment_length
    
    # self_weight
    @property
    def self_weight(self)->float:
        '''
        To calculate segment self weight in unit of pcf
        '''

        if self.foundation_material is None:
            return -1
        else:
            return self.cross_section.cross_section_area * self.foundation_material.unit_weight

        
        
        
    def calculate_side_resistance(self, effective_stress: float, fs: FactorOfSafetyDeepFoundation = None, 
                         alpha_override = None, beta_override = None):
        '''
        To calculate side resistance.
        Note: this is not unit resistance.
        
        Args:
            effective_stress (float): effective stress in unit of psf
            fs (FactorOfSafetyDeepFoundation): factor of safety object
            alpha_override (float): override the default used in calcualting 
        '''

        # establish SideResistance Obj
        side_resistance_obj = SideResistance(self.layer)

        side_resistance_unit = side_resistance_obj.side_resistance_unit(effective_stress, alpha_override, beta_override)
        side_resistance = side_resistance_unit * self.side_surface_area

        # Apply factor of safety when needed
        if not fs is None:
            side_resistance = side_resistance / fs.fs_deep_foundation_skin

        return side_resistance
        
    def calculate_end_resistance(self, fs: FactorOfSafetyDeepFoundation = None):
        '''
        To calculate end resistance.
        Note: this is not unit resistance.
        '''
        # estabhlish EndResistance Obj
        end_resistance_obj = EndResistance(self.layer)

        end_resistance_unit = end_resistance_obj.end_resistance_unit()
        end_resistance = end_resistance_unit * self.cross_section.cross_section_area

        if not fs is None:
            end_resistance = end_resistance / fs.fs_deep_foundation_end

        return end_resistance
    