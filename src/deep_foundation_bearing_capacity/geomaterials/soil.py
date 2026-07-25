# class for input soil parameters
import numpy as np

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial


class Soil(Geomaterial):
    def __init__(self, soil_index:int, unit_weight: float = 120, elastic_modulus: float = 0,
                  friction_angle:float = 0, cohesion:float = 0, n60: float= None,
                 soil_type_advanced: str = None):
        '''
        To initialize soil parameters

        Args:
            soil_index (int): unique material index
            unit_weight (float): unit weight in unit of pcf
            elastic_modulus (float): elastic modulus in unit of psf
            friction_angle (float): soil effective friction in unit of degree.
                                    For clay (cohesive), use zero
            cohesion (float): soil cohesion in unit of pound per square foot 
            soil_type_advanced (str): advanced soil type description
        '''
        
        super().__init__(unit_weight, elastic_modulus)
        
        self._sanity_check_friction_angle(friction_angle)
        self._sanity_check_cohesion(cohesion)
        self._sanity_check_friction_angle_cohesion(friction_angle, cohesion)
        self._sanity_check_n60(n60)

        '''
        soil_type_advanced_dict:
            gs: gravelly sand
            igm_cohesionless: cohesionless intermediate geomaterial
            igm_cohesive: cohesive intermediate geomaterial
        '''
        
        self.soil_type_advanced_dict = ["gs", "igm_cohesionless"]
        self._sanity_check_soil_type_advanced(soil_type_advanced, n60)
 
        self.soil_index = soil_index
        self.unit_weight = unit_weight
        self.friction_angle = friction_angle
        self.cohesion = cohesion
        self.n60 = n60


        # Soil type general (int)
        self.soil_type_general = self._determine_soil_type_general()

        # Soil type advanced (str)
        self.soil_type_advanced = soil_type_advanced

    @classmethod
    def from_dict(cls, data:dict):
        return cls(soil_index = int(data.get("soil_index")), 
                   unit_weight = float(data.get("unit_weight")), 
                   friction_angle = float(data.get("friction_angle")),
                   cohesion = float(data.get("cohesion")), 
                   n60 = data.get("n60"),
                   soil_type_advanced = data.get("soil_type_advanced"))



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
            raise ValueError("ERROR: friction_angle shall be zero or greater.")
            
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
    
    def _sanity_check_friction_angle_cohesion(self, friction_angle, cohesion):
        """
        Check friction_angle and cohesion at the same time.
        friction_angle and cohesion cannot be zero at the same time
        """
        if friction_angle == 0 and cohesion == 0:
            raise ValueError("ERROR: friction_angle and cohesion cannot be zero at the same time.")
        
        return True
    
    def _sanity_check_n60(self, n60):
        '''
        To perform sanity check on N60 blowcounts

        Args:
            n60: standard penetration blowcounts. Not corrected by effective stress 

        Returns:
            True if passes
        '''

        # sanity check on n60

        if not isinstance(n60, constants.NUMERIC_TYPES):
            raise TypeError("n60 data type shall be float, int, np.ndarray, np.generic.")
        
        if n60 is not None and np.min(np.asarray(n60)) < 0:
            raise ValueError("ERROR: n60 shall be zero or greater.")

        return True
    
    def _sanity_check_soil_type_advanced(self, soil_type_advanced:str, n60 = None):
        '''
        Sanity check on soil_type_advanced
        '''
 
        if soil_type_advanced is None:
            return True

        if not isinstance(soil_type_advanced, str):
            raise TypeError("Error: soil_type_advanced shall be str.")

        if soil_type_advanced not in self.soil_type_advanced_dict:
            raise ValueError("ERROR: input soil_type_advanced is undefined.")
        
        #if soil_type_advanced == "igm_cohesionless" and n60 is not None and n60 <50:
        #    raise ValueError("ERROR: cohesionless igm should have N60 greater than 50.")
        return True
    

    def modify_friction_angle(self, friction_angle_new):
        '''
        To modify self.friction_angle.
        '''
        self._sanity_check_friction_angle(friction_angle_new)
        self._sanity_check_friction_angle_cohesion(friction_angle_new, self.cohesion)

        self.friction_angle = friction_angle_new
        self.soil_type_general = self._determine_soil_type_general()

    def modify_cohesion(self, cohesion_new):
        '''
        To modify self.cohesion.
        '''
        self._sanity_check_cohesion(cohesion_new)
        self._sanity_check_friction_angle_cohesion(self.friction_angle, cohesion_new)

        self.cohesion = cohesion_new
        self.soil_type_general = self._determine_soil_type_general()

    def modify_soil_type_advanced(self, advanced_type: str)-> bool:
        '''
        To manually change soil type advanced
        '''
        self._sanity_check_soil_type_advanced(advanced_type)

        self.soil_type_advanced = advanced_type

        return True

    def _determine_soil_type_general(self)->int:
        '''
        To determine soil 
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
        
    def display_properties(self, properties = ["soil_index", "unit_weight", "cohesion", "friction_angle", "n60"]):
        '''
        To display specified soil properties

        Args:
            properties (list[str]): strs that match soil properties in the class
        '''

        for property in properties:
            print(f"{property} is: {getattr(self, property)}")
  


