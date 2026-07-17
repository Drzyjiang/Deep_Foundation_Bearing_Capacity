# unit resistance for deep foundations
import csv
from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np
import pandas as pd

from deep_foundation_bearing_capacity.constants.constants import ATM, FT2M, PSF2TSF, SCALAR_TYPE
from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial
from deep_foundation_bearing_capacity.geomaterials.layer import Layer
from deep_foundation_bearing_capacity.geomaterials.rock import Rock
from deep_foundation_bearing_capacity.geomaterials.soil import Soil

FILE_DIR = Path(__file__).parent

class SideResistance:
    '''
    Abtract class for SoilSideResistance and RockSideResistance
    '''
    
    @classmethod
    def for_material(cls, layer:Layer)->"SideResistance":
    
        if isinstance(layer.geomaterial, Soil):
            return SoilSideResistance(layer)
        elif isinstance(layer.geomaterial, Rock):
            return RockSideResistance(layer)
        
        raise TypeError(f"ERROR: layer.geomaterial {layer.geomaterial} is not supported.")
    
        

class RockSideResistance:
    '''
    To determine rock side resistance for deep foundations
    '''
    def __init__(self, layer):
        self.layer = layer

    def side_resistance_unit(self):
        '''
        Top wrapper for rock side resistance
        '''
        pass

    def _calculate_alpha(self, sigma_n = None ):
        '''
        To calculate alpha (empirical factor for cohesive igm, not for cohesive soil)
        Reference: FHWA Driller Shaft manual 99 Figure 11.5
        '''
        # sigma_n is pressure exerted by fluid concrete at the middle of layer
        if sigma_n is None:
            sigma_n = (self.layer.top_depth + self.layer.thickness * 0.5) * self.layer.geomaterial.density

        def find_closest(lst:list[float], target:float):
            '''
            find the index of closest value to a target in a list 
            
            Args:
                lst (list[float]): sorted list in ascending order
                                    len(lst) >= 2
            '''
            idx1, idx2 = sorted(range(len(lst), key = lambda i: abs(lst[i] - target)))[:2]

            if target <= lst[0] or target >= lst[-1]: # target is beyond lower and upper bounds of lst
                idx2 = idx1

            return idx1, idx2

        sigma_n_pa_ratio = sigma_n / ATM

        idx1, idx2 = find_closest(range(1,8), sigma_n_pa_ratio)

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
            xp = []
            yp = []
            df = pd.read_csv(alpha_curve_names[idx][1])

            # interpolate by qu
            alpha_values.append(np.interp(self.layer.geomaterial.qu, df.iloc[:,0], df.iloc[:,1]))
        
        # interpolate by sigma_n_pa_ratio

        return np.interp(sigma_n_pa_ratio, [alpha_curve_names[idx1][1], alpha_curve_names[idx2][1]], alpha_values)

    def _calculate_phi(self):
        '''
        To calculate joint-effect factor that accounts for the effect of open joints that
        are either filled or not.
        '''
        pass

    def side_resistance_unit_igm_cohesive(self):
        '''
        To calculate side resistance of cohesive IGM
        '''

        alpha = self._calculate_alpha()
        phi = self._calculate_phi()
        return alpha * phi * self.layer.geomaterial.qu

class SoilSideResistance:
    '''
    To determine soil side resistance for deep foundations
    '''
    def __init__(self, layer: Layer):
        self.layer = layer
    

    def side_resistance_unit(self, effective_stress: float, alpha_override: float = None, 
                             beta_override:float = None, uplift = False):
        '''
        Top wrapper for side resistance

        Args:
            effective_stress (float): effective stress in unit of psf
            alpha_override (float): override alpha when calculate side resistance for cohesive layer
            beta_override (float): override beta when calculate side resistance for cohesionless layer
            uplift (bool): whether side resistance is for uplift
        '''

        # sanity check on effective_stress
        # negative effective stress is currently not applicable
        if effective_stress < 0:
            raise ValueError("ERROR: negative effective stress is currently not applicable.")
        
        # sanity check on alpha_override
        if not alpha_override is None and (alpha_override < 0.45 or alpha_override > 0.55):
            raise ValueError("ERROR: typical alpha_override shall be between 0.45 and 0.55.")
        
        # sanity check on beta_override
        if not beta_override is None and (beta_override <0.25 or beta_override > 1.80):
            raise ValueError("ERROR: typical beta_override shall be between 0.25 and 1.80.")

        # judge by soil_type_advanced
        if self.layer.geomaterial.soil_type_advanced == "gs":
            return self.side_resistance_unit_cohesionless(effective_stress, beta_override, uplift)
        elif self.layer.geomaterial.soil_type_advanced == "igm_cohesionless":
            return self.side_resistance_unit_cohesionless(effective_stress, beta_override, uplift)

        # judge by soil_type_general
        if self.layer.geomaterial.soil_type_general == 1:
            return self.side_resistance_unit_cohesionless(effective_stress, beta_override, uplift)
        elif self.layer.geomaterial.soil_type_general == 2:
            return self.side_resistance_unit_cohesive(alpha_override, uplift)
        else:
            raise ValueError("ERROR: side_resistance_unit for current soil_type_general is yet to implement.")

    def _calculate_alpha(self):
        '''
        To caclulate alpha (ratio of adhesion to undrained shear strength) for cohesive soil
        Notes: depth-related correction is not applied here

        Returns:
            alpha (float)
        '''

        su_to_pa = self.layer.geomaterial.cohesion / ATM
        XP = [1.5, 2.5]
        YP = [0.55, 0.45]

        alpha = float(np.interp(su_to_pa, XP, YP))

        return alpha

    def _calculate_beta(self, effective_stress: SCALAR_TYPE)->SCALAR_TYPE:
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
            return self._calculate_ko(effective_stress) * np.tan(np.radians(self._calculate_phi_prime(effective_stress)))

        # determine based on soil_type_general
        if self.layer.geomaterial.soil_type_general == 1: # sand
            if self.layer.geomaterial.n60 >= 15:
                # note: when depth is in unit of foot, use coefficient of 0.135, not 0.245
                beta =  1.5 - 0.135 * depth_mid**0.5
            else:
                beta = (self.layer.geomaterial.n60 / 15.0) * (1.5 - 0.135 * depth_mid**0.5)
  
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
        deg = np.degrees(np.atan( (self.layer.geomaterial.n60/ (12.3 + 20.3 * effective_stress/ATM))**0.34 ))
        deg = min(deg, 45)

        return deg
    
    def _calculate_ko(self, effective_stress: SCALAR_TYPE):
        '''
        To calcualte earth pressure coefficient 
        '''
        phi_prime_rad = np.radians(self._calculate_phi_prime(effective_stress))
        ko = (1 - np.sin(phi_prime_rad)) * (0.2*ATM*self.layer.geomaterial.n60 / effective_stress)**(np.sin(phi_prime_rad))

        return ko

    def side_resistance_unit_cohesionless(self, effective_stress: float, beta_override:float = None, uplift:bool = False):
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

        if not beta_override is None:
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

        if not alpha_override is None:
            alpha = alpha_override
        else:
            alpha = self._calculate_alpha()

        side_resistance_cohesive = alpha * self.layer.soil.cohesion

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
    Class for end resistance of deep foundation
    This shall not be applied to shallow foundation
    '''
    def __init__(self, layer: Layer):
        self.layer = layer

    def end_resistance_unit(self):
        '''
        Top wrapper for end resistance
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

        XP = [500, 1000, 2000]
        YP = [6.5, 8.0, 9.0]
        N_ast = float(np.interp(self.layer.geomaterial.cohesion, XP, YP))
    
        return  N_ast * self.layer.geomaterial.cohesion


