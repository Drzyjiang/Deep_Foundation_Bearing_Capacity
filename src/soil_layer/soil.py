# class for input soil parameters
import numpy as np
from src.constants import constants

class soil:
    def __init__(self, unit_weight:float = 0, friction_angle:float = 0, cohesion:float = 0):
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

        self.unit_weight = unit_weight
        self.friction_angle = friction_angle
        self.cohesion = cohesion

    @classmethod
    def from_dict(cls, data:dict):
        return cls(unit_weight = data["unit_weight"], friction_angle = data["friction_angle"], cohesion = data["cohesion"])

    def _sanity_check_unit_weight(self, unit_weight):
        '''
        To perform sanity check on unit weight
        '''

        if isinstance(unit_weight, constants.NUMERIC_TYPES) == False:
            raise TypeError("unit_weight data type shall be float, int, np.ndarray, np.generic.")
        
        # sanity check on soil unit weight

        if np.min(np.asarray(unit_weight)) < constants.UNIT_WEIGHT_WATER:
            raise ValueError(f"ERROR: soil unit weight is unlikely smaller than water unit weight.")

        return True

    def _sanity_check_friction_angle(self, friction_angle):
        '''
        To perform sanity check on friction angle

        Args:
            friction_angle: soil effective friction in unit of degree.
                                    For clay (cohesive), use zero
        '''

        if isinstance(friction_angle, constants.NUMERIC_TYPES) == False:
            raise TypeError("unit_weight data type shall be float, int, np.generic, np.ndarray.")
        
        # sanity check on soil unit weight
        if np.min(np.asarray(friction_angle)) < 0:
            raise ValueError(f"ERROR: friction angle shall be zero or greater.")
        
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

        if isinstance(cohesion, constants.NUMERIC_TYPES) == False:
            raise TypeError("cohesion data type shall be float, int, np.ndarray, np.generic.")
        
        # sanity check on soil unit weight
        if np.min(np.asarray(cohesion)) < 0:
            raise ValueError(f"ERROR: cohesion shall be zero or greater.")

        
        return True
    
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



