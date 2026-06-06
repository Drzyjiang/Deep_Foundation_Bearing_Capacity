# class for layer parameters

from src.soil_layer.soil import soil
from src.constants import constants

class layer:
    def __init__(self, ground_water_depth:float, soil: soil = None, top_depth = None, thickness = None):
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

        # 

    def _sanity_check_ground_water_depth(ground_water_depth):
        '''
        To perform sanity check on ground_water_depth
        '''

        if not isinstance(ground_water_depth, constants.NUMERIC_TYPES):
            raise TypeError("ground_water_depth data type shall be float, int, np.ndarray, np.generic.")
    
        return True
        
    def _sanity_check_top_depth(top_depth):
        '''
        To perform sanity check on top_depth
        '''
        if not isinstance(top_depth, constants.NUMERIC_TYPES):
            raise TypeError("ground_water_depth data type shall be float, int, np.ndarray, np.generic.")
    
        return True
    
    def _sanity_check_thickness(thickness):
        '''
        To perform sanity check on thickness
        '''
        if not isinstance(thickness, constants.NUMERIC_TYPES):
            raise TypeError("thickness data type shall be float, int, np.ndarray, np.generic.")
        
        if thickness < 0:
            raise ValueError("Thickness shall be a non-negative value.")
    
        return True

