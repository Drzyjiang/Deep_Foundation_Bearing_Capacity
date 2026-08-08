# unit resistance for deep foundations
from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from deep_foundation_bearing_capacity.constants.constants import (
    ATM_APPROXIMATE,
    FT2M,
    PSF2MPA,
    PSF2TSF,
    SCALAR_TYPE,
    YIELD_STRENGTH_CONCRETE,
)
from deep_foundation_bearing_capacity.geomaterials.layer import Layer
from deep_foundation_bearing_capacity.geomaterials.rock import Rock
from deep_foundation_bearing_capacity.geomaterials.soil import Soil

FILE_DIR = Path(__file__).parent

@dataclass
class SideResistanceContext:
    """
    Input Parameters shared by RockSideResistance and SoilSideResistance
    """
    # Used by RockSideResistance
    
    # Used by SoilSideReistance
    # effective stress in unit of psf
    effective_stress: float

    # whether side resistance is for uplift
    uplift:float = False

    # override alpha when calculate side resistance for cohesive layer
    alpha_override: float = None

    # override beta when calculate side resistance for cohesionless layer
    beta_override:float = None


class SideResistance:
    '''
    Abtract class for SoilSideResistance and RockSideResistance
    '''
    def __init__(self, layer):
        self.layer = layer
    
    @classmethod
    def for_material(cls, layer:Layer)->"SideResistance":
     
        if isinstance(layer.geomaterial, Soil):
            return SoilSideResistance(layer)
        elif isinstance(layer.geomaterial, Rock):
            return RockSideResistance(layer)

      
        
        raise TypeError(f"ERROR: layer.geomaterial {layer.geomaterial} is not supported.")
    
    @abstractmethod
    def side_resistance_unit(self, side_resistance_context: SideResistanceContext):
        """
        Interface for unit side resistance
        """
        pass

class RockSideResistance(SideResistance):
    '''
    To determine rock side resistance for deep foundations
    '''
    def __init__(self, layer):
        super().__init__(layer)

    def side_resistance_unit(self, side_resistance_context:SideResistanceContext):
        '''
        Top wrapper for rock side resistance
        '''
        side_resistance_unit = None
        if self.layer.geomaterial.rock_type_advanced == "igm_cohesive":
            side_resistance_unit = self.side_resistance_unit_igm_cohesive(side_resistance_context)
        else:
            side_resistance_unit = self.side_resistance_unit_rock(side_resistance_context)
        
         # Apply uplift reduction
        if side_resistance_context.uplift:
            side_resistance_unit = side_resistance_unit * self._uplift_resistance_reduction()

        return side_resistance_unit

    def _calculate_alpha(self, sigma_n = None ):
        '''
        To calculate alpha (empirical factor for cohesive igm, not for cohesive soil)
        Reference: FHWA Driller Shaft manual 99 Figure 11.5, Eq.(11.23)
        sigma_n is pressure exerted by fluid concrete at the middle of layer
        sigma_n is estimated as 65% of total vertical stress at mid depth with constant unit weight 
        '''

        if sigma_n is None:
            # depth is capped at 12 m, 
            depth = min(12 / FT2M, self.layer.top_depth + self.layer.thickness * 0.5)
            sigma_n = 0.65 * depth * self.layer.geomaterial.unit_weight

        def find_closest(lst:list[float], target:float):
            '''
            find the index of closest value to a target in a list 
            
            Args:
                lst (list[float]): sorted list in ascending order
                                    len(lst) >= 2
            '''
            idx1, idx2 = sorted(list(range(len(lst))), key = lambda i: abs(lst[i] - target))[:2]

            if target <= lst[0] or target >= lst[-1]: # target is beyond lower and upper bounds of lst
                idx2 = idx1

            return idx1, idx2

        sigma_n_pa_ratio = sigma_n / ATM_APPROXIMATE

        idx1, idx2 = find_closest(list(range(1,8)), sigma_n_pa_ratio)

        # load digitized curve
        # first co
        alpha_curve_names = {0: (1, FILE_DIR/"cohesive_igm/alpha_sigman_pa_1.csv"), 
                             1: (2, FILE_DIR/"cohesive_igm/alpha_sigman_pa_2.csv"),
                             2: (3, FILE_DIR/"cohesive_igm/alpha_sigman_pa_3.csv"),
                             3: (4, FILE_DIR/"cohesive_igm/alpha_sigman_pa_4.csv"),
                             4: (5, FILE_DIR/"cohesive_igm/alpha_sigman_pa_5.csv"),
                             5: (6, FILE_DIR/"cohesive_igm/alpha_sigman_pa_6.csv"),
                             6: (7, FILE_DIR/"cohesive_igm/alpha_sigman_pa_7.csv"),
                             }

        alpha_values = []

        for idx in [idx1, idx2]:

            df = pd.read_csv(alpha_curve_names[idx][1])
         
            # interpolate by qu
            alpha_values.append(np.interp(self.layer.geomaterial.qu * PSF2MPA, df.iloc[:,0], df.iloc[:,1]))
      
        # Use Fig 11.5 to get alpha through interpolating by sigma_n_pa_ratio
        # use log(sigma_n_pa_ratio) instead of sigma_n_pa_ratio
        alpha = np.interp(np.log(sigma_n_pa_ratio), [np.log(alpha_curve_names[idx1][0]), 
                                                     alpha_curve_names[idx2][0]], alpha_values)
        alpha = alpha * np.tan(np.radians(self.layer.geomaterial.friction_angle)) / np.tan(np.radians(30))

        return alpha
        
    def _calculate_phi(self):
        '''
        To calculate joint-effect factor that accounts for the effect of open joints that
        are either filled or not.
        Reference: FHWA Drilled Shaft Manual 99 Table 11.4
        '''

        # sanity check
        if self.layer.geomaterial.rqd < 20:
            raise ValueError("ERROR: FHWA cannot recommend phi for cohesive IGM with RQD less than 20.")
        
        xp = [20.0, 30.0, 50.0, 70.0, 100.0]
        yp = None

        if self.layer.geomaterial.joint == "closed":
            yp = [0.45, 0.50, 0.60, 0.85, 1.00]
        elif self.layer.geomaterial.joint == "open":
            yp = [0.45, 0.50, 0.55, 0.55, 0.85]

        return np.interp(self.layer.geomaterial.rqd, xp, yp)
        

    def side_resistance_unit_igm_cohesive(self, side_reistance_context: SideResistanceContext):
        '''
        To calculate side resistance of cohesive IGM in unit of psf
        Reference: FHWA Drilled Shaft Manual 99 Eq.(11.21)
                   not Eq.(B.39)

        Args:
            side_resistance_context (SideResistanceContext):
            
        '''
        alpha = self._calculate_alpha()
        phi = self._calculate_phi()

        return alpha * phi * self.layer.geomaterial.qu
    
    def side_resistance_unit_rock(self, side_resistance_context: SideResistanceContext, uplift:bool = False):
        '''
        Top wrapper of side resistance of rock
        Assume smooth rock socket
        Reference: FHWA Drilled shaft manual 99 Eq.11.24
        Args:
            side_resistance_context (SideResistanceContext): context parameters for side resistance
            uplift (bool): whether side resistance is for uplift
        '''
        qu = min(self.layer.geomaterial.qu, YIELD_STRENGTH_CONCRETE)
        return 0.65 * ATM_APPROXIMATE * (qu/ATM_APPROXIMATE)**0.5
    
    def _uplift_resistance_reduction(self)->float:
        '''
        To derive reduction for uplift side resistance for rock.
        Reference: FHWA Drilled Shaft Manual 99 Eq.(11.30)
        rock, cohesive IGM: 1.00
        '''
        return 1.0


class SoilSideResistance(SideResistance):
    '''
    To determine soil side resistance for deep foundations
    '''
    def __init__(self, layer: Layer):
        super().__init__(layer)

    def side_resistance_unit(self, side_resistance_context: SideResistanceContext):
        '''
        Top wrapper for side resistance
            side_resistance_context (SideResistanceContext): all parameters for side resistance calculation
        '''
        # sanity check on effective_stress
        # negative effective stress is currently not applicable
        if side_resistance_context.effective_stress < 0:
            raise ValueError("ERROR: negative effective stress is currently not applicable.")
        
        # sanity check on alpha_override
        if side_resistance_context.alpha_override is not None and (
            side_resistance_context.alpha_override < 0.45 or side_resistance_context.alpha_override > 0.55):
            raise ValueError("ERROR: typical alpha_override shall be between 0.45 and 0.55.")
        
        # sanity check on beta_override
        if side_resistance_context.beta_override is not None and (
            side_resistance_context.beta_override <0.25 or side_resistance_context.beta_override > 1.80):
            raise ValueError("ERROR: typical beta_override shall be between 0.25 and 1.80.")

        # judge by soil_type_advanced
        if self.layer.geomaterial.soil_type_advanced == "gs":
            return self.side_resistance_unit_cohesionless(side_resistance_context.effective_stress,
                                                          side_resistance_context.beta_override,
                                                          side_resistance_context.uplift)
        elif self.layer.geomaterial.soil_type_advanced == "igm_cohesionless":
            return self.side_resistance_unit_cohesionless(side_resistance_context.effective_stress,
                                                          side_resistance_context.beta_override,
                                                          side_resistance_context.uplift)

        # judge by soil_type_general
        if self.layer.geomaterial.soil_type_general == 1:
            return self.side_resistance_unit_cohesionless(side_resistance_context.effective_stress,
                                                          side_resistance_context.beta_override,
                                                          side_resistance_context.uplift)
        elif self.layer.geomaterial.soil_type_general == 2:
            return self.side_resistance_unit_cohesive(side_resistance_context.alpha_override,
                                                      side_resistance_context.uplift)
        else:
            raise ValueError("ERROR: side_resistance_unit for current soil_type_general is yet to implement.")

    def _calculate_alpha(self):
        '''
        To caclulate alpha (ratio of adhesion to undrained shear strength) for cohesive soil
        Notes: depth-related correction is not applied here

        Returns:
            alpha (float)
        '''

        su_to_pa = self.layer.geomaterial.cohesion / ATM_APPROXIMATE
        XP = [1.5, 2.5]
        YP = [0.55, 0.45]
        
        alpha = float(np.interp(su_to_pa, XP, YP))

        return alpha

    def _calculate_beta(self, effective_stress: SCALAR_TYPE = 0)->SCALAR_TYPE:
        '''
        To calculate beta for cohesionless soil or gravelly sand/gravels
        Note: length is in unit of foot, NOT meter.

        Args:
            effective_stress (SCALAR_TYPE): 
        '''

        depth_mid = self.layer.top_depth + 0.5 * self.layer.thickness

        beta = 0

        # determine based on soil_type_advanced
        if self.layer.geomaterial.soil_type_advanced == "gs":
            if self.layer.geomaterial.n60 >= 15:
                beta = 2.0 - 0.15 * (depth_mid * FT2M)**0.75
            else:
                beta = (self.layer.geomaterial.n60 / 15.0) * (1.5 - 0.135 * depth_mid**0.5)

            # minimum beta is 0.25
            beta = max(beta, 0.25)

            # maximum beta is 1.80 for gravelly sand or gravels
            beta = min(beta, 1.80)
        elif self.layer.geomaterial.soil_type_advanced == "igm_cohesionless":
            return self._calculate_ko(effective_stress) * np.tan(
                np.radians(self._calculate_phi_prime(effective_stress)))

        # determine based on soil_type_general
        if self.layer.geomaterial.soil_type_general == 1: # sand
            if self.layer.geomaterial.n60 >= 15:
                beta =  1.5 - 0.245 * (depth_mid * FT2M)**0.5
            else:
                beta = (self.layer.geomaterial.n60 / 15.0) * (1.5 - 0.245 * (depth_mid *FT2M)**0.5)
  
            # minimum beta is 0.25
            beta = max(beta, 0.25)

            # maximum beta is 1.20 for sand
            beta = min(beta, 1.20)
  
        return beta
    
    def _calculate_phi_prime(self, effective_stress:SCALAR_TYPE)->SCALAR_TYPE:
        '''
        To estimate effective friction angle
        Reference: FHWA Drilled shaft manual 99, Equation 11.27

        Return:
            deg (SCALAR_TYPE): friction angle in unit of deg
        '''
        deg = np.degrees(np.atan( (self.layer.geomaterial.n60/ 
                                   (12.3 + 20.3 * effective_stress/ATM_APPROXIMATE))**0.34))
        deg = min(deg, 45)

        return deg
    
    def _calculate_ko(self, effective_stress: SCALAR_TYPE):
        '''
        To calcualte earth pressure coefficient 
        '''
        phi_prime_rad = np.radians(self._calculate_phi_prime(effective_stress))
        ko = (1 - np.sin(phi_prime_rad)) * (
            0.2*ATM_APPROXIMATE*self.layer.geomaterial.n60 / effective_stress)**(np.sin(phi_prime_rad))

        return ko

    def side_resistance_unit_cohesionless(self, effective_stress: float, 
                                          beta_override:float = None, uplift:bool = False):
        '''
        To calculate side resistance for cohesionless layer

        Args:
            effective_stress (float): effective stress 
            beta_override (float): override beta when calculate side resistance for cohesionless
            uplift (bool): whether side resistance is for uplift
                                    layer
        Returns:
            side_resistance_cohesionless (constants.SCALR_TYPE): side resistance of coheionless 
                                                                 soil in unit of psf

        '''

        if beta_override is not None:
            beta = beta_override
        else:
            beta = self._calculate_beta(effective_stress) 

        side_resistance_cohesionless = beta * effective_stress

        # obtain uplift reduction
        if uplift:
            uplift_reduction = self._uplift_resistance_reduction()
            side_resistance_cohesionless = side_resistance_cohesionless * uplift_reduction

        return side_resistance_cohesionless
    
    def side_resistance_unit_cohesive(self, alpha_override:float = None, uplift: bool = False)->float:
        '''
        To calculate side resistance for cohesive layer

        Args:
            alpha_override (float): override alpha when calculate side resistance for cohesive layer

        Returns:
            side_resistance_cohesionless (constants.SCALR_TYPE): side resistance of coheionless soil in unit of psf
        '''

        if alpha_override is not None:
            alpha = alpha_override
        else:
            alpha = self._calculate_alpha()

        side_resistance_cohesive = alpha * self.layer.geomaterial.cohesion

        # apply uplift reduction
        if uplift:
            uplift_reduction = self._uplift_resistance_reduction()
            side_resistance_cohesive = side_resistance_cohesive * uplift_reduction

        return side_resistance_cohesive
    
    def _uplift_resistance_reduction(self)->float:
        '''
        To derive reduction for uplift side resistance.
        Sand, gravelly sand, cohesionless IGM: 0.75
        Clay, rock, cohesive IGM: 1.00
        '''
        if self.layer.geomaterial.soil_type_general == 1 or (
            self.layer.geomaterial.soil_type_advanced == "igm_cohesionless") or (
            self.layer.geomaterial.soil_type_advanced == "gs"):   
            return 0.75
        else:
            return 1.0


class EndResistance:
    '''
    Abtract class for SoilEndResistance and RockEndResistance
    '''
    @classmethod
    def for_material(cls, layer:Layer)->"SideResistance":
        '''
        
        '''
        if isinstance(layer.geomaterial, Soil):
            return SoilEndResistance(layer)
        elif isinstance(layer.geomaterial, Rock):
            return RockEndResistance(layer)
        raise TypeError(f"ERROR: layer.geomaterial {layer.geomaterial} is not supported.")
    
    @abstractmethod
    def end_resistance_unit(self, context):
        '''
        Interface of unit end resistance
        '''
        pass

@dataclass
class EndResistanceContext:
    """
    All parameters for SoilEndResistance and RockEndResistance
    """
    # parameters for rock
    socket_width_ratio: float = 1.0

    # parameters for soil

    
class RockEndResistance(EndResistance):
    def __init__(self, layer: Layer, socket_width_ratio: float = 1.0):
        '''
        Args:
            layer (Layer): layer
            socket_width_ratio (float): socket length to foundation width/diamater ratio
        '''
        if socket_width_ratio < 0.0:
            raise ValueError("ERROR: socket-to-width ratio shall be a non-negative value.")

        self.layer = layer
        self.socket_width_ratio = socket_width_ratio

    def end_resistance_unit(self, end_resistance_context):
        '''
        Top wrapper for rock unit end resistance

        Args:
            end_resistance_context (): parameters for both SoilEndResistance and RockEndResistance
        '''
        if self.layer.geomaterial.rock_type_advanced == "igm_cohesive":
            return self.end_resistance_unit_igm_coheisve()
        else:
            return self.end_resistance_unit_rock()
    
    def end_resistance_unit_igm_coheisve(self):
        '''
        Calculate unit end resistance for cohesive IGM.
        The value is the same as rock
        '''
        return self.end_resistance_unit_rock()

    def end_resistance_unit_rock(self):
        '''
        Calculate unit end resistance for rock
        Reference: FHWA Drilled Shaft Manual 99 Eq.(11.5) through (11.7)
        '''
        if self.socket_width_ratio >= 1.5 and self.layer.geomaterial.rqd == 100: # FHWA 99 Eq.(11.5)
            return self.layer.geomaterial.qu * 2.5
        elif self.layer.geomaterial.joint == "closed" and self.layer.geomaterial.rqd >= 70 and (
            self.layer.geomaterial.qu >5.2 / PSF2TSF): # FHWA 99 (Eq. 11.6)
            
            return 4.83 * (self.layer.geomaterial.qu * PSF2MPA)**0.51 / PSF2MPA
        else: # FHWA 99 (Eq.11.7)
            s = self.get_s()
            m = self.get_m()
            return (s**0.5 + (m*(s**0.5)+s)**0.5) * self.layer.geomaterial.qu

    def get_s(self):
        '''
        Derive rock mass quality parameter s
        Reference: FHWA Drilled Shaft Manual 99 Table 11.2    
        '''
        rock_quality_s_dict = {"Excellent": 1.0,
                               "Very good": 0.1,
                               "Good": 4e-2,
                               "Fair": 1e-4,
                               "Poor": 1e-5,
                                "Very poor": 0
                                }

        return rock_quality_s_dict.get(self.layer.geomaterial.rock_quality)
    
    def get_m(self):
        '''
        Derive rock mass quality parameter m
        Reference: FHWA Drilled Shaft Manual 99 Table 11.2
        '''
        rock_quality_m_dict = {}
        rock_quality_m_dict["Excellent"] = {"A": 7.0, "B": 10.0, "C": 15.0, "D": 17.0, "E": 25.0}
        rock_quality_m_dict["Very good"] = {"A": 3.5, "B": 5.0,  "C": 7.5,  "D": 8.5,  "E": 12.5}
        rock_quality_m_dict["Good"]      = {"A": 0.7, "B": 1.0,  "C": 1.5,  "D": 1.7,  "E": 2.5}
        rock_quality_m_dict["Fair"]      = {"A": 0.14,"B": 0.2,  "C": 0.3,  "D": 0.34, "E": 0.5}
        rock_quality_m_dict["Poor"]      = {"A": 0.04,"B": 0.05, "C": 0.08, "D": 0.09, "E": 0.13}
        rock_quality_m_dict["Very poor"] = {"A": 0.007,"B":0.01, "C": 0.015,"D": 0.017,"E": 0.025}

        return rock_quality_m_dict.get(self.layer.geomaterial.rock_quality).get(
            self.layer.geomaterial.rock_type)

class SoilEndResistance(EndResistance):
    '''
    Class for soil end resistance of deep foundation
    This shall not be applied to shallow foundation
    '''
    def __init__(self, layer: Layer):
        self.layer = layer

    def end_resistance_unit(self, end_resistance_context = EndResistanceContext()):
        '''
        Top wrapper for end resistance

        Args:
            end_resistance_content: parameters for both SoilEndResistance and RockEndResistance
        '''

        if self.layer.geomaterial.soil_type_general == 1:
            return self.end_resistance_unit_cohesionless()
        elif self.layer.geomaterial.soil_type_general == 2:
            return self.end_resistance_unit_cohesive() 

    def end_resistance_unit_cohesionless(self):
        '''
        To calculate end unit resistance of cohesionless layer 
        Reference: FHWA Drilled Shaft Manual 99,  Eq.(11.4b)
        '''
        # Sanity check on layer.geomaterial.n60
        if self.layer.geomaterial.n60 < 0:
            raise ValueError("ERROR: cohesionless soil shall not have negative N60.")

        return  min(0.60 * self.layer.geomaterial.n60, 30) / PSF2TSF
    
    def end_resistance_unit_cohesive(self):
        '''
        To calculate end unit resistance of cohesive layer
        Notes: depth-related correction is not applied
        Reference: FHWA Driller Shaft Manual 99, Eq.(11.2)
        '''
        # data points faciliating interpolation
        # XP: undrained shear strength in psf
        # YP: N* in psf
        XP = [500, 1000, 2000]
        YP = [6.5, 8.0, 9.0]
        N_ast = float(np.interp(self.layer.geomaterial.cohesion, XP, YP))
    
        return  N_ast * self.layer.geomaterial.cohesion


