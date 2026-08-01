# class for layer parameters

from deep_foundation_bearing_capacity.constants.constants import NUMERIC_TYPE
from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial


class Layer:
    def __init__(self, layer_index: NUMERIC_TYPE, geomaterial: Geomaterial = None, ground_water_depth:NUMERIC_TYPE = 0,
                  top_depth: NUMERIC_TYPE = None, thickness: NUMERIC_TYPE = None):
        '''
        To initialize layer parameters

        Args:
            layer_index (int): a unique index for current layer
            geomaterial (Geomaterial): geomaterial object
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
        self.geomaterial = geomaterial

        # depth of top of the layer
        self.top_depth = top_depth

        # thickness of the layer
        self.thickness = thickness

    @classmethod
    def from_dict(cls, data:dict):
        '''
        Initialize by dict
        '''
        return cls(layer_index = data.get("layer_index"),
                   ground_water_depth = data.get("ground_water_depth"),
                   geomaterial = data.get("geomaterial"),
                   top_depth = data.get("top_depth"),
                   thickness = data.get("thickness")
                   )



    def _sanity_check_layer_index(self, layer_index):
        '''
        To perform sanity check on layer_index
        '''
        pass

    def _sanity_check_ground_water_depth(self, ground_water_depth: NUMERIC_TYPE):
        '''
        To perform sanity check on ground_water_depth
        '''
        if ground_water_depth is None:
            return True
      
        if not isinstance(ground_water_depth, NUMERIC_TYPE):
            raise TypeError("ground_water_depth data type shall be float, int, np.ndarray, np.generic.")
    
        return True
        
    def _sanity_check_top_depth(self, top_depth):
        '''
        To perform sanity check on top_depth
        '''
        if top_depth is None:
            return True

        if not isinstance(top_depth, NUMERIC_TYPE):
            raise TypeError("ground_water_depth data type shall be float, int, np.ndarray, np.generic.")
    
        return True
    
    def _sanity_check_thickness(self,thickness):
        '''
        To perform sanity check on thickness
        '''
        if thickness is None:
            return True

        if not isinstance(thickness, NUMERIC_TYPE):
            raise TypeError("thickness data type shall be float, int, np.ndarray, np.generic.")
        
        if thickness < 0:
            raise ValueError("layer thickness shall be a non-negative value.")
    
        return True


    
    def display_properties(self, properties = ["layer_index", "ground_water_depth", "top_depth", "thickness"], 
                           display_geomaterial:bool = False):
        '''
        To display layer properties
        
        Args:
            properties (list[str]): layer property to diplay
            print_geomaterial (bool): whether to plot geomaterial properties
        '''

        for property in properties:
            print(f"{property} is: {getattr(self, property)}")

        if display_geomaterial:
            self.geomaterial.display_properties()

