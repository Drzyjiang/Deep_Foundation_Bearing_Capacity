# Classes for deep foundations
from functools import cached_property

from deep_foundation_bearing_capacity.constants.constants import SCALAR_TYPE
from deep_foundation_bearing_capacity.segments.segments import Segment


class DeepFoundation:
    def __init__(self, segments: list[Segment], top_depth: SCALAR_TYPE = 0, resistance_correction:bool = True):
        '''
        Args:
            segments (Segment): list a of segments, in order of from top to bottom 
        '''

        self._sanity_check_segments(segments)  
        self._sanity_check_top_depth(top_depth) 

        self.segments = segments
        self.top_depth = top_depth

        self.resistance_correction = resistance_correction

        # apply correction
        if resistance_correction:
            self._correction_side_resistance()

    def _sanity_check_segments(self, segments: list[Segment])->bool:
        '''
        Sanity check on segments
        '''

        if not isinstance(segments, list):
            raise TypeError("ERROR: segments shall be a list")
        
        for segment in segments:
            if not isinstance(segment, Segment):
                raise TypeError("ERROR: all segments shall be type Segment.")
            
        return True
    
    def _sanity_check_top_depth(self, top_depth: SCALAR_TYPE)->bool:
        '''
        Sanity check on top depth
        
        '''
        if not isinstance(top_depth, SCALAR_TYPE):
            raise TypeError(f"ERROR: top_depth shall be type {SCALAR_TYPE}")
        
        return True
    
    def _segment_mid_depth(self):
        '''
        To calculate mid depth of each segment
        '''
        segment_mid_depth = []
        mid_depth = 0

        for segment in self.segments:
            # update mid_depth by increment upper half of thickness
            mid_depth = mid_depth + segment.layer.thickness / 2.0

            segment_mid_depth.append(mid_depth)

            # update mid_depth by increment lower half of thickness
            mid_depth = mid_depth + segment.layer.thickness / 2.0
        
        return segment_mid_depth
    
    def _segment_bottom_depth(self):
        '''
        To calculate bottom depth of each segment
        '''
        segment_bottom_depth = []
        bottom_depth = 0

        for segment in self.segments:
            bottom_depth = bottom_depth + segment.layer.thickness
            segment_bottom_depth.append(bottom_depth)

        return segment_bottom_depth
    
    def _segment_top_depth(self):
        '''
        To calculate top depth of each segment
        '''
        segment_top_depth = []
        top_depth = 0

        for segment in self.segments:
            segment_top_depth.append(top_depth)
            top_depth = top_depth + segment.layer.thickness

        return segment_top_depth
    
    @cached_property
    def _calculate_segments_side_resistance(self, corrections = None)->list[float]:
        '''
        To calculate side resistance of each segment

        Args:
            corrections: list of SideResistanceCorrection and EndResistanceCorrection objects
        '''
        # collect all default side resistance
        segment_side_resistances = []

        for segment in self.segments:
            segment_side_resistances.append(segment.calculate_side_resistance())
        
        # apply correction
        segment_bottom_depth_values = self._segment_bottom_depth()
        segment_top_depth_values = self._segment_top_depth()

        for correction in corrections:
            segment_side_resistances = correction.apply_all(segment_side_resistances,
                                                            segment_bottom_depth_values,
                                                            segment_top_depth_values
                                                            )

        return segment_side_resistances


    def _accumulative_side_resistance(self):
        '''
        To calcualte accumulative side resistance
        '''

class SideResistanceCorrections:
    '''
    Methods to correct side resistance only
    '''
    def __init__(self,segments:Segment):
        
        self.segments = segments
    
    def apply_all(self,  segment_side_resistances, segment_bottom_depth_values, 
                  segment_top_depth_values, applications = ["depth"]):
        '''
        Args:
            applications (list[str]): list of strs that describe applicable functions
        '''
        for application in applications:
            segment_side_resistances = getattr(self, application)(segment_side_resistances,
                                                                  segment_bottom_depth_values,
                                                                  segment_top_depth_values)
        return segment_side_resistances

    def depth(self, segment_side_resistances, segment_bottom_depth_values, segment_top_depth_values):
        '''
        depth related correction

        '''    
        segment_side_resistances_corrected = []

        # Between the ground surface and 5 ft, alpha is set to zero
        # to account for seasonal moisture change
        MOISTURE_CHANGE_DEPTH = 5.0
        ABOVE_PILE_BASE = 5.0
        for segment_side_resistance_original, segment, segment_bottom_depth_value, segment_top_depth_value in zip(
            segment_side_resistances, self.segments, 
            segment_bottom_depth_values, segment_top_depth_values):
            if segment_bottom_depth_value <= MOISTURE_CHANGE_DEPTH or (
                segment_top_depth_value >= segment_bottom_depth_value - ABOVE_PILE_BASE):
                # Need to re-calculate unit resistance by overriding alpha
                segment_side_resistances_corrected.append(segment.calculate_side_resistance(alpha_override=0))
            else: # no change
                segment_side_resistances_corrected.append(segment_side_resistance_original)

        return segment_side_resistances_corrected
                
            