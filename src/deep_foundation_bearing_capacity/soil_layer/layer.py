# class for layer parameters

from deep_foundation_bearing_capacity.constants import constants
from deep_foundation_bearing_capacity.soil_layer.soil import Soil


class Layer:
    def __init__(self, layer_index: int, soil: Soil = None, ground_water_depth:float = 0, top_depth: float = None, thickness: float = None):
        '''
        To initialize layer parameters

        Args:
            layer_index (int): a unique index for current layer
            soil (Soil): soil object
            ground_water_depth (float): ground water depth in unit of float
            top_depth (float): depth of upper side of layer
            thickness (float): thickness of layer
        '''

        self._sanity_check_layer_index(layer_index)
        self._sanity_check_ground_water_depth(ground_water_depth)
        self._sanity_check_top_depth(top_depth)
        self._sanity_check_thickness(thickness)

        self.layer_index = layer_index

        # ground water table
        self.ground_water_depth = ground_water_depth
        self.soil = soil

        # depth of top of the layer
        self.top_depth = top_depth

        # thickness of the layer
        self.thickness = thickness


    def _sanity_check_layer_index(self, layer_index):
        '''
        To perform sanity check on layer_index
        '''

        if not isinstance(layer_index, int):
            raise TypeError("layer_index shall be type int.")
        else:
            return True

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


    
    def display_properties(self, properties = ["layer_index", "ground_water_depth", "top_depth", "thickness", "effective_stress_mid"]):
        '''
        To display layer properties
        '''

        for property in properties:
            print(f"{property} is: {getattr(self, property)}")


