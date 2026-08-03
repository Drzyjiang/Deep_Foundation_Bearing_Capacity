# classes for segments

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.constants.constants import REDUCTION_ASD_CONCRETE_COMPRESSION
from deep_foundation_bearing_capacity.cross_sections.cross_sections import CrossSection
from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import FactorOfSafetyDeepFoundation
from deep_foundation_bearing_capacity.foundation.foundation_material import FoundationConcrete, FoundationMaterial
from deep_foundation_bearing_capacity.geomaterials.layer import Layer
from deep_foundation_bearing_capacity.segments.unit_resistance import (
    EndResistance,
    EndResistanceContext,
    SideResistance,
    SideResistanceContext,
)


class Segment:
    '''
    Segment accounts for not only cross section and section_length, 
    but also layer and side resistance and end bearing
    One segment corresponds to only one layer and one cross_section.
    
    '''
    def __init__(self, cross_section: CrossSection, layer: Layer, 
                 foundation_material:FoundationMaterial = None):
        '''
        
        '''
        # segment length is layer's thickness
        self.segment_length = layer.thickness

        # cross section type
        self.cross_section = cross_section

        # layer
        self.layer = layer

        # foundation material
        self.foundation_material = foundation_material

        # establish SideResistance Obj
        self.side_resistance_obj = SideResistance.for_material(self.layer)

        # estabhlish EndResistance Obj
        self.end_resistance_obj = EndResistance.for_material(self.layer)

        
    @property
    def side_surface_area(self):
        '''
        # calculate side surface area
        
        '''
        return self.cross_section.perimeter * self.segment_length
    
    
    @property
    def self_weight_total(self)->float:
        '''
        To calculate segment self total weight in unit of pcf
        '''

        if self.foundation_material is None:
            return -1
        else:
            return self.foundation_material.unit_weight * (self.cross_section.area
                                                            * self.segment_length) 

    @property
    def self_weight_effective(self)->float:
        '''
        To calculate segment self effective weight in unit of pcf
        '''

        if self.foundation_material is None:
            return -1
        else:
            dry_thickness = min(max(self.layer.ground_water_depth - self.layer.top_depth, 0), self.layer.thickness)
            saturated_thickness = min(max(self.layer.top_depth+self.layer.thickness -
                                           self.layer.ground_water_depth, 0), self.layer.thickness)

            return self.cross_section.area * (self.foundation_material.unit_weight
                    * dry_thickness + (self.foundation_material.unit_weight - 
                    constants.UNIT_WEIGHT_WATER) * saturated_thickness)         
        
        
    def calculate_side_resistance(self, side_resistance_context: SideResistanceContext):
        '''
        To calculate side resistance.
        Note: this is not unit resistance.
        
        Args:
            side_resistance_context (SideResistanceContext)
        '''

        side_resistance_unit = self.side_resistance_obj.side_resistance_unit(side_resistance_context)
        side_resistance = side_resistance_unit * self.side_surface_area

        return side_resistance
    

        
    def calculate_end_resistance(self, end_resistance_context: EndResistanceContext):
        '''
        To calculate end resistance.
        Note: this is not unit resistance.
        '''
        end_resistance_unit = self.end_resistance_obj.end_resistance_unit(end_resistance_context)
        end_resistance = end_resistance_unit * self.cross_section.area

        return end_resistance
    
    def structural_compression_capacity(self):
        '''
        To caclulate structural compression capacity
        '''

        # sanity check
        if isinstance(self.foundation_material, FoundationConcrete):
            # TODO
            return self.structural_compression_capacity_concrete()
        else:
            raise ValueError("Current FoundationMaterial type is not implemented yet.")
    
    def structural_compression_capacity_concrete(self):
        '''
        To calculate structural compression capacity for pure concrete cross-section
        Note: by allowable stress design (ASD)
        '''
        #
        return REDUCTION_ASD_CONCRETE_COMPRESSION * (
            self.cross_section.area * self.foundation_material.yield_strength)