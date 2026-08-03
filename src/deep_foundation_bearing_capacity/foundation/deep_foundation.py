# Classes for deep foundations
from functools import cached_property

import matplotlib
import matplotlib.pyplot as plt

from deep_foundation_bearing_capacity.constants.constants import SCALAR_TYPE, UNIT_WEIGHT_WATER
from deep_foundation_bearing_capacity.factor_of_safety.factor_of_safety import FactorOfSafetyDeepFoundation
from deep_foundation_bearing_capacity.segments.segments import Segment
from deep_foundation_bearing_capacity.segments.unit_resistance import EndResistanceContext, SideResistanceContext


class DeepFoundation:
    def __init__(self, segments: list[Segment], top_depth: SCALAR_TYPE = 0, 
                 resistance_corrections=None, fs: FactorOfSafetyDeepFoundation = None):
        '''
        Args:
            segments (Segment): list a of segments, in order of from top to bottom 
                                note that segments can have different segment.layer.ground_water_depth,
                                to account for potential artesian  
            top_depth (SCALAR_TYPE): upper depth of the first segment. This overrides segments[0].top_depth
            resistance_corrections (list[]): list of SideResistanceCorrection Obj and/or EndResistanceCorrection Obj
            fs (FactorOfSafetyDeepFoundation): factor of safety
        '''
        
        self._sanity_check_segments(segments)  
        self._sanity_check_top_depth(top_depth) 

        self.segments = segments
        self.top_depth = top_depth

        # correction to side resistance and end resistance
        self.resistance_corrections = resistance_corrections or []

        # factor of safety
        self.fs = fs

        
    @property
    def effective_weight(self):
        '''
        calculate deep foundation effective self weight in unit of pound
        '''
        return self.calculate_segment_weights_effective_accumulative()[-1]
    
    def calculate_segment_weights_effective_accumulative(self)->list[float]:
        '''
        To calculate accumulative effective self_weight of segments.
        '''
        segment_weights_effective_accumulative = []
        segment_weight_effective_accumulative = 0

        for segment in self.segments:
            segment_weight_effective_accumulative = (segment_weight_effective_accumulative +
                                                      segment.self_weight_effective)
            segment_weights_effective_accumulative.append(segment_weight_effective_accumulative)
        
        return segment_weights_effective_accumulative


    def _sanity_check_segments(self, segments: list[Segment])->bool:
        '''
        Sanity check on segments
        '''

        if not isinstance(segments, list):
            raise TypeError("ERROR: segments shall be a list")
        
        for segment in segments:
            if not isinstance(segment, Segment):
                raise TypeError(f"ERROR: all segments shall be type {Segment}.")
            
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
                                    segment.segment_length /2.0 * segment.layer.geomaterial.unit_weight) 
            segment_total_stresses.append(segment_total_stress)
            segment_total_stress = segment_total_stress + (
                                    segment.segment_length /2.0 * segment.layer.geomaterial.unit_weight)

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
    def calculate_segment_side_resistances(self, uplift: bool = False)->list[float]:
        '''
        To calculate side resistance of each segment

        Args:
            uplift (bool): whether side resistance is for uplift
        '''
        # collect all default side resistance
        segment_side_resistances = []

        for segment, effective_stress in zip(self.segments, self.calculate_segment_effective_stresses):
            side_resistance_context = SideResistanceContext(
                effective_stress = effective_stress,
                uplift = uplift
            )
            segment_side_resistances.append(segment.calculate_side_resistance(side_resistance_context))

        # apply factor of safety
        if uplift == False:
            fs = self.fs.fs_side_compression
        else:
            fs = self.fs.fs_side_uplift
        segment_side_resistances = [x / fs for x in segment_side_resistances]
        
        # apply correction
        segment_bottom_depth_values = self._segment_bottom_depths()
        segment_top_depth_values = self._segment_top_depths()
        for correction in self.resistance_corrections:
            segment_side_resistances = correction.apply_all(segment_side_resistances,
                                                            segment_bottom_depth_values,
                                                            segment_top_depth_values
                                                            )
     
        return segment_side_resistances
    
    def calculate_segment_end_resistances(self)->list[float]:
        '''
        To caclulate segment end resistances in unit of psf

        Args:
            fs (float): factor of safety for end resistance
        '''
        # calculate unfactored resistances
        segment_end_resistances = []
        for segment in self.segments:
            end_resistance_context = EndResistanceContext()
            segment_end_resistance = segment.calculate_end_resistance(end_resistance_context)
            segment_end_resistances.append(segment_end_resistance)

        # apply factor of safety
        segment_end_resistances = [x/ self.fs.fs_end for x in segment_end_resistances]

        return segment_end_resistances

    def calculate_segment_side_resistances_accumulative(self, uplift:bool = False)->list[float]:
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

        for segment_side_resistance in self.calculate_segment_side_resistances( uplift = uplift):
            accumulative = accumulative + segment_side_resistance
            segment_side_resistances_accumulative.append(accumulative)

        return segment_side_resistances_accumulative
    
    def calculate_compression_resistances_accumulative(self)->list[float]:
        '''
        To calculate accumulative compression resistance.
        Note: each entire segment is included, not just half segment

        Args:
            fs: factor of safety for side resistance

        Returns:
            (list[float]): list of accumulative compression resistance

        '''

        segment_side_resistances_accumlative = self.calculate_segment_side_resistances_accumulative(uplift = False)
        segment_end_resistances = self.calculate_segment_end_resistances()

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
        segment_weights_accumulative = self.calculate_segment_weights_effective_accumulative()

        uplift_resitances_accumulative = [a+b for a, b in zip(segment_side_resistances_accumulative,
                                                                         segment_weights_accumulative)]
        return uplift_resitances_accumulative
    
    def segments_structural_capacity_compression(self):
        '''
        To calculate structural compression capacity of all segments
        '''

        segments_structural_capacity = []
        for segment in self.segments:
            segments_structural_capacity.append(segment.structural_compression_capacity())
        
        return segments_structural_capacity


    def visualize_resistances_accumulative(self, fs:float = 1.0, target = "compression", style = "piecewise"):
        '''
        Visualize accumulative compression or uplift resistance 

        Args:
            fs (float): factor of safety for side resistance and end resistance
            target (str): either "compression" or "uplift"
            style (str): select plot style from ["piecewise", "mid"]
                        "piecewise": 
        '''
        style_options = ["piecewise", "mid"]
        # sanity check on style arg
        if style not in style_options:
            raise ValueError(f"ERROR: sytle shall be selected from {style_options}")
        
        # sanity_check on target
        if target != "compression" and target != "uplift":
            raise ValueError(f"ERROR: target shall be either 'compression' or 'uplift'.")

        if target == "compression":
            resistances_accumulative = self.calculate_compression_resistances_accumulative()
        elif target == "uplift":
            resistances_accumulative = self.calculate_uplift_resistances_accumulative()
        
        fig, ax = plt.subplots()

        if style == "piecewise":
            self._visualize_resistances_accumulative_piecewise(ax, target, resistances_accumulative)
        elif style == "mid":
            self._visualize_resistance_accumulative_mid(ax, target, resistances_accumulative)
        else:
            raise ValueError(f"ERROR: style {style} is undefined.")

        plt.close(fig)

        return fig

    
    def _visualize_resistances_accumulative_piecewise(self, 
                                                      ax: matplotlib.axes.Axes, target: str, 
                                                      resistances_accumulative:list[float])->(
                                                       matplotlib.figure.Figure):
        '''
        To visualize accumulative compression resistance in piecewise style

        Args:
            ax (matplotlib.axes.Axes): ax handle
            target (str): either "compression" or "uplift"
            resistances_accumulative (list[float]): accumulative resistances of each segment

        Returns:
            fig (matplotlib.figure.Figure)
        '''
        
        segment_top_depths = self._segment_top_depths()
        segment_bottom_depths = self._segment_bottom_depths()

        # form ys by alternating segment_top_depths and segment_bottom_depths
        ys = [y for pair in zip(segment_top_depths, segment_bottom_depths) for y in pair]

        # form xs by shallow copy
        xs = [x/1000.0 for x in resistances_accumulative for _ in range(2)]
        
        ax.plot(xs, ys)
        ax.set_xlabel(f"Accumulative {target} resistance [kip]")
        ax.invert_yaxis()
        ax.set_ylabel("Depth [ft]")
        ax.grid(True)
      
        for xi, yi in zip(xs, ys):
            ax.annotate(text = f"{xi:.0f}", xy=(xi, yi), textcoords = "offset points", xytext = (5,5), fontsize = 8)
       
    
    def _visualize_resistance_accumulative_mid(self, ax: matplotlib.axes.Axes, 
                                               target: str, resistance_accumulative)->(
                                                   matplotlib.figure.Figure
                                               ):
        '''
        To visualize accumulative resistance at mid of each segment.
        Note that even though resistance at shown at mid of segment, side resistance of 
        lower half segment is already included.

        Args:
            ax (matplotlib.axes.Axes): ax handle
            target (str): either "compression" or "uplift"
            resistances_accumulative (list[float]): accumulative resistances of each segment
        '''
        ys = self._segment_mid_depths()
        xs = [x/1000.0 for x in resistance_accumulative]

        ax.plot(xs, ys)
        ax.set_xlabel(f"Accumulative {target} resistance [kip]")
        ax.invert_yaxis()
        ax.set_ylabel("Depth [ft]")
        ax.grid(True)

        for xi, yi in zip(xs, ys):
            ax.annotate(text =f"{xi:.0f}", xy=(xi, yi), textcoords="offset points",xytext = (5,5), fontsize = 8)
        

class SideResistanceCorrections:
    '''
    TODO: NOT TESTED YET
    Methods to correct side resistance only
    '''
    def __init__(self,segments:Segment):
        
        self.segments = segments
    
    def apply_all(self,  segment_side_resistances, segment_bottom_depth_values, 
                  segment_top_depth_values, applications = ["correct_moist_change"]):
        '''
        Args:
            applications (list[str]): list of strs that describe applicable functions
        '''
        for application in applications:
            segment_side_resistances = getattr(self, application)(segment_side_resistances,
                                                                  segment_bottom_depth_values,
                                                                  segment_top_depth_values)
        return segment_side_resistances

    def correct_moisture_change(self, segment_side_resistances, segment_bottom_depth_values, segment_top_depth_values):
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
                
            