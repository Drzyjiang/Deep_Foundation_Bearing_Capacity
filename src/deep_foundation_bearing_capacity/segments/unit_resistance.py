# unit resistance for deep foundations
from deep_foundation_bearing_capacity.constants.constants import PSF2TSF
from deep_foundation_bearing_capacity.soil_layer.layer import Layer
from deep_foundation_bearing_capacity.soil_layer.soil import Soil


class SideResistance:
    '''
    To determine side resistance for deep foundations
    '''
    def __init__(self, layer: Layer):
    
        self.layer = layer

    def side_resistance_unit(self):
        '''
        Top wrapper for side resistance
        '''

        if self.layer.soil.soil_type_general == 1:
            return self.side_resistance_unit_cohesionless()
        elif self.layer.soil.soil_type_general == 2:
            return 



    def _calculate_beta(self):
        '''
        To calculate beta.
        Note: length is in unit of foot, NOT meter.
        '''

        depth_mid = self.layer.top_depth + 0.5 * self.layer.thickness

      
        if self.layer.soil.n60 >= 15:
            # note: when depth is in unit of foot, use coefficient of 0.135, not 0.245
            return 1.5 - 0.135 * depth_mid**0.5
        else:
            return (self.layer.soil.n60 / 15.0) * (1.5 - 0.135 * depth_mid**0.5)

    def side_resistance_unit_cohesionless(self):
        '''
        To calculate side resistance for cohesionless layer

        Returns:
            side_resistance_cohesionless (constants.SCALR_TYPE): side resistance of coheionless soil in unit of psf
        '''

        # references = [""]

        # sanity check
        if self.layer.soil.soil_type_general != 1:
            raise ValueError("ERROR: soil type is not cohesionless.")

        beta = self._calculate_beta() 

        return beta * self.layer.effective_stress_mid

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
            return     

    def end_resistance_unit_cohesionless(self):
        '''
        To calculate end unit resistance of cohesionless layer 
        Reference: FHWA Drilled Shaft Manual 99,  Eq.(11.4b)
        '''

        # Sanity check on layer.soil.n60
        if self.layer.soil.n60 < 0:
            raise ValueError("ERROR: cohesionless soil shall not have negative N60.")

        return  min(0.60 * self.layer.soil.n60, 30) / PSF2TSF

