# Classes for deep foundations

from deep_foundation_bearing_capacity.segments.segments import Segment


class deep_foundation:
    def __init__(self, segments: list[Segment], top_depth: float = 0):
        '''
        Args:
            segments (Segment): list a of segments, in order of from top to bottom 
        '''

        self._sanity_check_on_segments(segments)   

        self.segments = segments



    def _sanity_check_on_segments(self, segments: list[Segment])->bool:
        '''
        Sanity check on segments
        '''

        if not isinstance(segments, list):
            raise TypeError("ERROR: segments shall be a list")
        
        for segment in segments:
            if not isinstance(segment, Segment):
                raise TypeError("ERROR: all segments shall be type Segment.")
            
        return True
    
    

    def _accumulative_side_resistance(self):
        '''
        To calcualte accumulative side resistance
        '''