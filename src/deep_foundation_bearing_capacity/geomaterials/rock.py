# classes for rock 
# Currently not including cohesionless IGM
from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial


class Rock(Geomaterial):
    def __init__(self, qu: float = None, rqd: float = None, rock_type:str = None,
                 rock_quality: str = None):
        '''
        A class for (competent) rock material.

        Args:
            qu (float): unconfined compressive strength in unit of psf
            rqd (float):
            rock_type (str): one from ["A", "B", "C", "D", "E"]
                            Reference: FHWA Drilled Shaft Manual Table 11.2
                            A: Carbonate rocks with well-developed crystal cleavage (e.g., 
                            dolostone, limestone, marble)
                            B: Lithified argillaeous rocks (mudstone, siltstone, shale,
                              slate)
                            C: Arenaceous rocks (sandstone, quartzite)
                            D: Fine-grained igneous rocks (andesite, dolerite, diabase,
                              rhyolite)
                            E: Coarse-grained igneous and metamorphic rocks (amphibole, 
                               garbro, gnesis, granite, norite, quartz-diorite)
            rock_quality (str): one from ["Excellent", "Very good", "Good", "Fair", "Poor", 
                                     "Very poor"]

        '''
        self.rock_type_options = ["A", "B", "C", "D", "E"]
        self.rock_quality_options = ["Excellent", "Very good", "Good", "Fair", "Poor", 
                                     "Very poor"]

        # unconfined compression strength in unit of psf
        self.qu = qu

        # rock quality designation
        self.rqd = rqd

        # rock type
        self.rock_type = rock_type

        # rock quality
        self.rock_quality = rock_quality

    def _sanity_check_qu(self, qu:float)->bool:
        '''
        To perform sanity check on qu
        '''
        if(qu <= 0):
            raise ValueError("ERROR: rock qu shall be a positive value.")
        else:
            return True
    
    def _sanity_check_rqd(self, rqd:float)->bool:
        '''
        To perform sanity check on rock quality designation
        '''
        if(rqd < 0):
            raise ValueError("ERROR: rock RQD shall be a non-negative value.")
        else:
            return True
        
    def _sanity_check_rock_type(self, rock_type:str)->bool:
        '''
        To perform sanity check on rock_type
        '''
        

        if rock_type not in self.rock_type_options:
            raise ValueError(f"ERROR: rock_type shall be one from {self.rock_type_options}.")
        else:
            return True
    
    def _sanity_check_rock_quality(self, rock_quality:str = None)->bool:
        '''
        To perform sanity check on rock_quality.
        '''
        rock_quality_options = ["Excellent", "Very good", "Good", "Fair", "Poor", "Very poor"]

        if rock_quality not in self.rock_quality_options:
            raise ValueError(f"ERROR: rock_quality shall be one from {self.rock_quality_options}")
        else:
            return True
