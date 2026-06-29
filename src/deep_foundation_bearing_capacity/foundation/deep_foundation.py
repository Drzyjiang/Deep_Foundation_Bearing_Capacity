# Classes for deep foundations

from deep_foundation_bearing_capacity.constants.constants import SCALAR_TYPE
from deep_foundation_bearing_capacity.segments.segments import Segment


class DeepFoundation:
    def __init__(self, segments: list[Segment], top_depth: SCALAR_TYPE = 0, resistance_correction:bool = True):
        '''
        Args:
            segments (Segment): list a of segments, in order of from top to bottom 
        '''

        self._sanity_check_on_segments(segments)   

        self.segments = segments

    



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
    
    def _side_resistance_correction(self):
        '''
        To correct side resistance of each segment 
        '''

    def _side_resistance_correction_depth(self, segments: list[Segment]):
        '''
        To correct side resistance due to depth
        '''    

        # Between the ground surface and 5 ft, alpha is set to zero
        # to account for seasonal moisture change


    def _accumulative_side_resistance(self):
        '''
        To calcualte accumulative side resistance
        '''