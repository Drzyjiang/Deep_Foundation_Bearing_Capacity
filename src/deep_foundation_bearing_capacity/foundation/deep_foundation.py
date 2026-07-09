# Classes for deep foundations
from functools import cached_property

import matplotlib.pyplot as plt

from deep_foundation_bearing_capacity.constants.constants import SCALAR_TYPE, UNIT_WEIGHT_WATER
from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import FactorOfSafetyDeepFoundation
from deep_foundation_bearing_capacity.segments.segments import Segment


class DeepFoundation:
    def __init__(self, segments: list[Segment], top_depth: SCALAR_TYPE = 0, 
                 resistance_corrections=None):
        '''
        Args:
            segments (Segment): list a of segments, in order of from top to bottom 
                                note that segments can have different segment.layer.ground_water_depth,
                                to account for potential artesian  
            top_depth (SCALAR_TYPE): upper depth of the first segment. This overrides segments[0].top_depth
            resistance_corrections (list[]): list of SideResistanceCorrection Obj and/or EndResistanceCorrection Obj
        '''

        self._sanity_check_segments(segments)  
        self._sanity_check_top_depth(top_depth) 

        self.segments = segments
        self.top_depth = top_depth

        # correction to side resistance and end resistance
        self.resistance_corrections = resistance_corrections or []

        
    @property
    def total_weight(self):
        '''
        calculate deep foundation self weight in unit of pound
        '''

        return self.calculate_segment_weights_accumulative()[-1]
    
    def calculate_segment_weights_accumulative(self)->list[float]:
        '''
        To calculate accumulative self_weight of segments.
        '''
        segment_weights_accumulative = []
        segment_weight_accumulative = 0

        for segment in self.segments:
            segment_weight_accumulative = segment_weight_accumulative + segment.self_weight
            segment_weights_accumulative.append(segment_weight_accumulative)
        
        return segment_weights_accumulative


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
    
    def _segment_mid_depths(self):
        '''
        To calculate mid depth of each segment
        '''
        segment_mid_depths = []
        mid_depth = 0

        for segment in self.segments:
            # update mid_depth by increment upper half of segment length
            mid_depth = mid_depth + segment.segment_length / 2.0

            segment_mid_depths.append(mid_depth)

            # update mid_depth by increment lower half of segment length
            mid_depth = mid_depth + segment.segment_length  / 2.0
        
        return segment_mid_depths
    
    def _segment_bottom_depths(self):
        '''
        To calculate bottom depth of each segment
        '''
        segment_bottom_depths = []
        bottom_depth = 0

        for segment in self.segments:
            bottom_depth = bottom_depth + segment.segment_length 
            segment_bottom_depths.append(bottom_depth)

        return segment_bottom_depths
    
    def _segment_top_depths(self):
        '''
        To calculate top depth of each segment
        '''
        segment_top_depths = []
        top_depth = 0

        for segment in self.segments:
            segment_top_depths.append(top_depth)
            top_depth = top_depth + segment.segment_length 

        return segment_top_depths
    
    def calculate_segment_total_stresses(self)->list[float]:
        '''
        To calculate total stresses at the mid depth of each segment

        Returns:
            segment_total_stresses (list[float]): total stresses at mid of each segment
        '''
        segment_total_stress = 0
        segment_total_stresses = []

        for segment in self.segments:
            segment_total_stress = segment_total_stress + (
                                    segment.segment_length /2.0 * segment.layer.soil.unit_weight) 
            segment_total_stresses.append(segment_total_stress)
            segment_total_stress = segment_total_stress + (
                                    segment.segment_length /2.0 * segment.layer.soil.unit_weight)

        return segment_total_stresses
    
    @cached_property
    def calculate_segment_effective_stresses(self):
        '''
        To calculate effective stresses at the mid depth of each segment
        '''

        segment_effective_stresses = []
        segment_effective_stress = 0

        segment_mid_depths = self._segment_mid_depths()
        
        segment_total_stresses = self.calculate_segment_total_stresses()

        for segment, segment_total_stress, segment_mid_depth in zip(
            self.segments, segment_total_stresses, segment_mid_depths):

            water_weight = UNIT_WEIGHT_WATER * (max(0, segment_mid_depth - segment.layer.ground_water_depth))
            segment_effective_stress = segment_total_stress - water_weight
            segment_effective_stresses.append(segment_effective_stress)
        
        return segment_effective_stresses
    
    #@cached_property
    def calculate_segment_side_resistances(self, fs: float = 1.0, uplift:bool = False)->list[float]:
        '''
        To calculate side resistance of each segment

        Args:
            fs (FactorOfSafetyDeepFoundation): factor of safety for deep foundations
            uplift (bool): False for compression; True for uplift
        '''
        # collect all default side resistance
        segment_side_resistances = []

        for segment, effective_stress in zip(self.segments, self.calculate_segment_effective_stresses):
            segment_side_resistances.append(segment.calculate_side_resistance(effective_stress, fs=fs, uplift=uplift))
        
        # apply correction
        segment_bottom_depth_values = self._segment_bottom_depths()
        segment_top_depth_values = self._segment_top_depths()

        for correction in self.resistance_corrections:
            segment_side_resistances = correction.apply_all(segment_side_resistances,
                                                            segment_bottom_depth_values,
                                                            segment_top_depth_values
                                                            )
     
        return segment_side_resistances
    
    def calculate_segment_end_resistances(self, fs:float = 1.0)->list[float]:
        '''
        To caclulate segment end resistances in unit of psf

        Args:
            fs (float): factor of safety for end resistance
        '''
        segment_end_resistances = []
        for segment in self.segments:
            segment_end_resistance = segment.calculate_end_resistance()
            # apply factor of safety
            segment_end_resistance = segment_end_resistance / fs

            segment_end_resistances.append(segment_end_resistance)

        return segment_end_resistances



    def calculate_segment_side_resistances_accumulative(self, fs:float = 1.0, uplift:bool = False)->list[float]:
        '''
        To calcualte moving accumulative side resistances

        Args:
            fs (float): factor of safety for side resistance
            uplift (bool): False for compression; True for uplift

        Returns:
            (list[float]): accumulative side resistance starting from top
        '''
        
        accumulative = 0
        segment_side_resistances_accumulative = []

        for segment_side_resistance in self.calculate_segment_side_resistances(fs = fs, uplift = uplift):
            accumulative = accumulative + segment_side_resistance
            segment_side_resistances_accumulative.append(accumulative)

        return segment_side_resistances_accumulative
    
    def calculate_compression_resistances_accumulative(self, fs:float = 1.0)->list[float]:
        '''
        To calculate accumulative compression resistance.
        Note: each entire segment is included, not just half segment

        Args:
            fs: factor of safety for side resistance

        Returns:
            (list[float]): list of accumulative compression resistance

        '''

        segment_side_resistances_accumlative = self.calculate_segment_side_resistances_accumulative(fs = fs)
        segment_end_resistances = self.calculate_segment_end_resistances(fs =fs)

        return [a + b for 
                a, b in zip(segment_side_resistances_accumlative, segment_end_resistances)]
    


    
    def calculate_uplift_resistances_accumulative(self)->list[float]:
        '''
        To calculate accumulative uplift resistance.
        Note: need to apply reduction factor to side resistance to account for 
        reduced lateral earth pressure coefficient

        Returns:
            uplift_resitances_accumulative (list[float]): accmulative uplift resistances
        '''
        
        
        segment_side_resistances_accumulative = self.calculate_segment_side_resistances_accumulative(uplift = True)
        segment_weights_accumulative = self.calculate_segment_weights_accumulative()

        uplift_resitances_accumulative = [a+b for a, b in zip(segment_side_resistances_accumulative,
                                                                         segment_weights_accumulative)]
        return uplift_resitances_accumulative
    
    def visualize_compression_resistances_accumulative(self, fs:float = 1.0, style = "piecewise"):
        '''
        Visualize accumulative compression resistance 

        Args:
            fs (float): factor of safety for side resistance and end resistance
            style (str): select plot style from ["piecewise", "mid"]
                        "piecewise": 
        '''
        style_options = ["piecewise", "mid"]
        # sanity check on style arg
        if not style in style_options:
            raise ValueError(f"ERROR: sytle shall be selected from {style_options}")
        


        compression_resistances_accumulative = self.calculate_compression_resistances_accumulative()


    def visualize_compression_resistances_accumulative_piecewise(self):
        '''
        To visualize accumulative compression resistance in piecewise style
        
        '''
        compression_resistances_accumulative = self.calculate_compression_resistances_accumulative()
        segment_top_depths = self._segment_top_depths()
        segment_bottom_depths = self._segment_bottom_depths()

        # form ys by alternating segment_top_depths and segment_bottom_depths
        ys = [y for pair in zip(segment_top_depths, segment_bottom_depths) for y in pair]

        # form xs by shallow copy
        xs = [x for x in compression_resistances_accumulative for _ in range(2)]

        plt.plot([x/1000.0 for x in xs], ys)
        plt.xlabel("Accumulative compression resistance [kip]")
        plt.gca().invert_yaxis()
        plt.ylabel("Depth [ft]")
        plt.grid(True)
        


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
                
            