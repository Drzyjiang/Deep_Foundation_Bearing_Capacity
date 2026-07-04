# class for input soil parameters
import numpy as np

from deep_foundation_bearing_capacity.constants import constants


class Soil:
    def __init__(self, unit_weight:float = 0, friction_angle:float = 0, cohesion:float = 0, n60: float=-1,
                 soil_type_advanced = None):
        '''
        To initialize soil parameters

        Args:
            unit_weight: soil unit weight in unit of pound per cubic foot
            friction_angle: soil effective friction in unit of degree.
                                    For clay (cohesive), use zero
            cohesion: soil cohesion in unit of pound per square foot 
        
        '''
        
        self._sanity_check_unit_weight(unit_weight)
        self._sanity_check_friction_angle(friction_angle)
        self._sanity_check_cohesion(cohesion)
        self._sanity_check_n60(n60)
        self._sanity_check_soil_type_advanced(soil_type_advanced)

        self.unit_weight = unit_weight
        self.friction_angle = friction_angle
        self.cohesion = cohesion
        self.n60 = n60

        # Soil type general (int)
        self.soil_type_general = self._determine_soil_type()

        # Soil type advanced (str)
        self.soil_type_advanced = soil_type_advanced

    @classmethod
    def from_dict(cls, data:dict):
        return cls(unit_weight = float(data["unit_weight"]), friction_angle = float(data["friction_angle"]),
                    cohesion = float(data["cohesion"]), n60 = data["n60"])

    def _sanity_check_unit_weight(self, unit_weight):
        '''
        To perform sanity check on unit weight
        '''

        if not isinstance(unit_weight, constants.NUMERIC_TYPES):
            raise TypeError("unit_weight data type shall be float, int, np.ndarray, np.generic.")
        
        # sanity check on soil unit weight

        if np.min(np.asarray(unit_weight)) < constants.UNIT_WEIGHT_WATER:
            raise ValueError("ERROR: soil unit weight is unlikely smaller than water unit weight.")

        return True

    def _sanity_check_friction_angle(self, friction_angle):
        '''
        To perform sanity check on friction angle

        Args:
            friction_angle: soil effective friction in unit of degree.
                                    For clay (cohesive), use zero
        '''

        if not isinstance(friction_angle, constants.NUMERIC_TYPES):
            raise TypeError("unit_weight data type shall be float, int, np.generic, np.ndarray.")
        
        # sanity check on soil unit weight
        if np.min(np.asarray(friction_angle)) < 0:
            raise ValueError("ERROR: friction angle shall be zero or greater.")
        
        return True
    
    def _sanity_check_cohesion(self, cohesion):
        '''
        To perform sanity check on cohesion

        Args:
            cohesion: soil cohesion in unit of pound per square foot 

        Returns:
            True if passes
        '''

        # sanity check on soil cohesion

        if not isinstance(cohesion, constants.NUMERIC_TYPES):
            raise TypeError("cohesion data type shall be float, int, np.ndarray, np.generic.")
        
        # sanity check on soil unit weight
        if np.min(np.asarray(cohesion)) < 0:
            raise ValueError("ERROR: cohesion shall be zero or greater.")

        
        return True
    
    def _sanity_check_n60(self, n60):
        '''
        To perform sanity check on N60 blowcounts

        Args:
            n60: standard penetration blowcounts. Not corrected by effective stress 

        Returns:
            True if passes
        '''

        # sanity check on soil cohesion

        if not isinstance(n60, constants.NUMERIC_TYPES):
            raise TypeError("n60 data type shall be float, int, np.ndarray, np.generic.")
        
        # sanity check on soil unit weight
        if np.min(np.asarray(n60)) < 0:
            raise ValueError("ERROR: n60 shall be zero or greater.")

        
        return True
    
    def _sanity_check_soil_type_advanced(self, soil_type_advanced):
        '''
        Sanity check on soil_type_advanced
        Valid list:
            gs: gravelly sand
            igm: intermediate geomaterial
        '''
        soil_type_advanced_dict = ["gs", "igm_coheionless", "igm_cohesive"]

        if soil_type_advanced is None:
            return True

        if not isinstance(soil_type_advanced, str):
            raise TypeError("Error: soil_type_advanced shall be str.")

        if soil_type_advanced not in soil_type_advanced_dict:
            raise ValueError("ERROR: input soil_type_advanced is undefined.")
    
    def modify_unit_weight(self, unit_weight_new):
        '''
        To modify self.unit_weight.
        '''

        self._sanity_check_unit_weight(unit_weight_new)

        self.unit_weight = unit_weight_new

    def modify_friction_angle(self, friction_angle_new):
        '''
        To modify self.friction_angle.
        '''

        self._sanity_check_friction_angle(friction_angle_new)

        self.friction_angle = friction_angle_new

    def modify_cohesion(self, cohesion_new):
        '''
        To modify self.cohesion.
        '''

        self._sanity_check_cohesion(cohesion_new)

        self.cohesion = cohesion_new

    def modify_soil_type_advanced(self, advanced_type: str)-> bool:
        '''
        To manually change soil type of gravelly sand (Type 3)
        '''
        self.soil_type_general = advanced_type

        return True

    def _determine_soil_type(self)->int:
        '''
        To determine soil 
        Type -1 (cohesion == 0 and friction_angle == 0): error
        Type 0 (cohesion !=0 and friction_angle !=0): mixed of cohesionless and cohesive. This case is RARE in calculation.
        Type 1 (cohesion == 0): cohesionless only, sand.
        Type 2 (cohesion != 0): cohesive only, clay.
        
        '''
        if self.friction_angle !=0 and self.cohesion !=0:
            return 0
        elif self.cohesion ==0 :
            return 1
        else:
            return 2
        
    
  


