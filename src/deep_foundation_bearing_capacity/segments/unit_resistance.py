# unit resistance for deep foundations
import numpy as np

from deep_foundation_bearing_capacity.constants.constants import ATM, PSF2TSF
from deep_foundation_bearing_capacity.soil_layer.layer import Layer
from deep_foundation_bearing_capacity.soil_layer.soil import Soil


class SideResistance:
    '''
    To determine side resistance for deep foundations
    '''
    def __init__(self, layer: Layer):
    
        self.layer = layer

    def side_resistance_unit(self, alpha_override: float = None, beta_override:float = None):
        '''
        Top wrapper for side resistance

        Args:
            alpha_override (float): override alpha when calculate side resistance for cohesive layer
            beta_override (float): override beta when calculate side resistance for cohesionless layer
        '''

        if self.layer.soil.soil_type_general == 1:
            return self.side_resistance_unit_cohesionless(beta_override)
        elif self.layer.soil.soil_type_general == 2:
            return self.side_resistance_unit_cohesive(alpha_override)
        else:
            raise ValueError("ERROR: side_resistance_unit for current soil_type_general is yet to implement.")

    def _calculate_alpha(self):
        '''
        To caclulate alpha (ratio of adhesion to undrained shear strength) for cohesive soil
        Notes: depth-related correction is not applied here

        Returns:
            alpha (float)
        '''

        su_to_pa = self.layer.soil.cohesion / ATM
        XP = [1.5, 2.5]
        YP = [0.55, 0.45]

        alpha = float(np.interp(su_to_pa, XP, YP))

        return alpha

    def _calculate_beta(self):
        '''
        To calculate beta for cohesionless soil
        Note: length is in unit of foot, NOT meter.
        '''

        depth_mid = self.layer.top_depth + 0.5 * self.layer.thickness

      
        if self.layer.soil.n60 >= 15:
            # note: when depth is in unit of foot, use coefficient of 0.135, not 0.245
            return 1.5 - 0.135 * depth_mid**0.5
        else:
            return (self.layer.soil.n60 / 15.0) * (1.5 - 0.135 * depth_mid**0.5)

    def side_resistance_unit_cohesionless(self, beta_override:float = None):
        '''
        To calculate side resistance for cohesionless layer

        Args:
            beta_override (float): override beta when calculate side resistance for cohesionless
                                    layer
        Returns:
            side_resistance_cohesionless (constants.SCALR_TYPE): side resistance of coheionless 
                                                                 soil in unit of psf

        '''

        if not beta_override is None:
            beta = beta_override
        else:
            beta = self._calculate_beta() 

        return beta * self.layer.effective_stress_mid
    
    def side_resistance_unit_cohesive(self, alpha_override:float = None):
        '''
        To calculate side resistance for cohesive layer

        Args:
            alpha_override (float): override alpha when calculate side resistance for cohesive layer

        Returns:
             (constants.SCALR_TYPE): side resistance of coheionless soil in unit of psf
        '''

        if not alpha_override is None:
            alpha = alpha_override
        else:
            alpha = self._calculate_alpha()

        return alpha * self.layer.soil.cohesion

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

        if self.layer.soil.soil_type_general == 1:
            return self.end_resistance_unit_cohesionless()
        elif self.layer.soil.soil_type_general == 2:
            return self.end_resistance_unit_cohesive() 

    def end_resistance_unit_cohesionless(self):
        '''
        To calculate end unit resistance of cohesionless layer 
        Reference: FHWA Drilled Shaft Manual 99,  Eq.(11.4b)
        '''

        # Sanity check on layer.soil.n60
        if self.layer.soil.n60 < 0:
            raise ValueError("ERROR: cohesionless soil shall not have negative N60.")

        return  min(0.60 * self.layer.soil.n60, 30) / PSF2TSF
    
    def end_resistance_unit_cohesive(self):
        '''
        To calculate end unit resistance of cohesive layer
        Notes: depth-related correction is not applied
        Reference: FHWA Driller Shaft Manual 99, Eq.(11.2)
        '''

        XP = [500, 1000, 2000]
        YP = [6.5, 8.0, 9.0]
        N_ast = float(np.interp(self.layer.soil.cohesion, XP, YP))
    
        return  N_ast * self.layer.soil.cohesion


