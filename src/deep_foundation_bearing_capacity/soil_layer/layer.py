# class for layer parameters

from src.constants import constants
from src.soil_layer.soil import soil


class layer:
    def __init__(self, soil: soil = None, ground_water_depth:float = 0, top_depth = None, thickness = None):
        '''
        To initialize layer parameters

        Args:
            ground_water_depth (float): ground water depth in unit of float 
        '''

        self._sanity_check_ground_water_depth(ground_water_depth)
        self._sanity_check_top_depth(top_depth)
        self._sanity_check_thickness(thickness)

        # ground water table
        self.ground_water_depth = ground_water_depth
        self.soil = soil

        # depth of top of the layer
        self.top_depth = top_depth

        # thickness of the layer
        self.thickness = thickness


        # calculate effective vertical stress at mid point
        self.effective_stress_mid = self._calculate_effective_stress(self.top_depth + 0.5 * self.thickness)


        


    def _sanity_check_ground_water_depth(self, ground_water_depth):
        '''
        To perform sanity check on ground_water_depth
        '''

        if not isinstance(ground_water_depth, constants.NUMERIC_TYPES):
            raise TypeError("ground_water_depth data type shall be float, int, np.ndarray, np.generic.")
    
        return True
        
    def _sanity_check_top_depth(self, top_depth):
        '''
        To perform sanity check on top_depth
        '''
        if not isinstance(top_depth, constants.NUMERIC_TYPES):
            raise TypeError("ground_water_depth data type shall be float, int, np.ndarray, np.generic.")
    
        return True
    
    def _sanity_check_thickness(self,thickness):
        '''
        To perform sanity check on thickness
        '''
        if not isinstance(thickness, constants.NUMERIC_TYPES):
            raise TypeError("thickness data type shall be float, int, np.ndarray, np.generic.")
        
        if thickness < 0:
            raise ValueError("Thickness shall be a non-negative value.")
    
        return True

    def _calculate_effective_stress(self, depth_target):
        '''
        To calculate vertical effective stress at a given depth of the layer

        Args:
            depth_target (constants.SCALAR_TYPE): depth at which effective stress to be calcualted

        Returns:
            effective vertical stress: in unit of psf
        '''

        depth_target = self.top_depth + 0.5 * self.thickness

        if depth_target <= self.ground_water_depth:
            return depth_target * self.soil.unit_weight
        else:
            return (self.ground_water_depth * self.soil.unit_weight +
                    (depth_target - self.ground_water_depth) *(self.soil.unit_weight - constants.UNIT_WEIGHT_WATER))
        