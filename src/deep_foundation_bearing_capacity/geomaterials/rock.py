# classes for rock
# Currently not including cohesionless IGM
from deep_foundation_bearing_capacity.geomaterials.geomaterial import Geomaterial


class Rock(Geomaterial):
    def __init__(self, rock_index, unit_weight: float = 150, elastic_modulus: float = 0,
                 friction_angle: float = None, qu: float = None, rqd: float = None,
                 rock_type:str = None, rock_quality: str = None, rock_type_advanced: str = None,
                 joint: str = "open"):
        '''
        A class for (competent) rock material.

        Args:
            rock_index (int): unique material identifier
            qu (float): unconfined compressive strength in unit of psf
            rqd (float): rock quality designation, no unit, between [0,100]
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

            rock_type_advanced (str): one from [None, "igm_cohesive"]

            rock_friction_angle (float): rock friction angle

            joint (str): either "closed" or "open"
        '''
        super().__init__(unit_weight, elastic_modulus)

        self.rock_type_options = ["A", "B", "C", "D", "E"]
        self.rock_quality_options = ["Excellent", "Very good", "Good", "Fair", "Poor",
                                     "Very poor"]
        self.rock_type_advanced_options = ["igm_cohesive", None]

        # sanity check on qu
        self._sanity_check_qu(qu, rock_type_advanced)

        # sanity check on rqd
        self._sanity_check_rqd(rqd)

        # sanity check on rock type
        self._sanity_check_rock_type(rock_type)

        # sanity_check on rock_quality
        self._sanity_check_rock_quality(rock_quality)

        # sanity_check on rock_type_advanced
        self._sanity_check_rock_type_advanced(rock_type_advanced)

        # sanity_check on joint
        self._sanity_check_joint(joint)

        # rock index
        self.rock_index = rock_index

        # rock friction angle
        self.friction_angle = friction_angle

        # unconfined compression strength in unit of psf
        self.qu = qu

        # rock quality designation
        self.rqd = rqd

        # rock type
        self.rock_type = rock_type

        # rock quality
        self.rock_quality = rock_quality

        # rock_type_advanced
        self.rock_type_advanced = rock_type_advanced

        # joint
        self.joint = joint

    @classmethod
    def from_dict(cls, data:dict):
        '''
        Initialize class using dict
        '''
        return cls(rock_index = int(data.get("rock_index")),
                   rqd = float(data.get("rqd")),
                   unit_weight = float(data.get("unit_weight")),
                   elastic_modulus = float(data.get("elastic_modulus", 0)),
                   friction_angle = float(data.get("friction_angle")),
                   qu = float(data.get("qu")),
                   rock_type = str(data.get("rock_type")),
                   rock_quality = str(data.get("rock_quality")),
                   rock_type_advanced = data.get("rock_type_advanced"),
                   joint = str(data.get("joint"))
                   )


    def _sanity_check_qu(self, qu:float, rock_type_advanced:str)->bool:
        '''
        To perform sanity check on qu

        Args:
            qu (float): rock unconfined compressive strength in psf
            rock_type_advanced (str): descriptor
        '''
        if qu is None:
            return True

        if(qu <= 0):
            raise ValueError("ERROR: rock qu shall be a positive value.")
        elif rock_type_advanced == "igm_cohesive":
            if qu <1e4:
                raise ValueError("ERROR: cohesive IGM shall have qu no less than 10,000 psf")
            elif qu > 1e5:
                raise ValueError("ERROR: cohesive IGM typically has qu less than 100,000 psf")
        else:
            return True

    def _sanity_check_rqd(self, rqd:float)->bool:
        '''
        To perform sanity check on rock quality designation
        '''
        if rqd is None:
            return True

        if rqd < 0:
            raise ValueError("ERROR: rock RQD shall be a non-negative value.")
        elif rqd > 100:
            raise ValueError("ERROR: rock RQD shall be less than 100.")
        else:
            return True

    def _sanity_check_rock_type(self, rock_type:str)->bool:
        '''
        To perform sanity check on rock_type
        '''

        if rock_type == "None":
            raise TypeError("ERROR: rock_type_advanced cannot be 'None'. Should be None")

        if rock_type is not None and rock_type not in self.rock_type_options:
            raise ValueError(f"ERROR: rock_type shall be one from {self.rock_type_options}.")
        else:
            return True

    def _sanity_check_rock_quality(self, rock_quality:str = None)->bool:
        '''
        To perform sanity check on rock_quality.
        '''

        if isinstance(rock_quality, str) and rock_quality == "None":
            raise TypeError("ERROR: rock_type_advanced cannot be 'None'")

        if rock_quality is not None and rock_quality not in self.rock_quality_options:
            raise ValueError(f"ERROR: rock_quality shall be one from {self.rock_quality_options}")
        else:
            return True

    def _sanity_check_rock_type_advanced(self, rock_type_advanced:str)->bool:
        '''
        To perform sanity check on rock_type_advanced
        '''
        if rock_type_advanced == "None":
            raise ValueError("ERROR: rock_type_advanced cannot be 'None'. Should be None")

        if (rock_type_advanced is not None) and (rock_type_advanced not in self.rock_type_advanced_options):
            raise ValueError(f"ERROR: rock_type_advanced shall be one from {self.rock_type_advanced_options}")

        return True

    def _sanity_check_joint(self, joint:str)->bool:
        '''
        To perform sanity check on joint
        '''

        if joint is not None and joint != "open" and joint != "closed":
            raise ValueError("ERROR: joint shall be either 'open' or 'closed'")

        return True

    def display_properties(self, properties = None):
        '''
        To display specified soil properties

        Args:
            properties (list[str]): strs that match rock properties in the class
        '''

        if properties is None:
            properties = ["rock_index", "unit_weight", "friction_angle", "qu", "rqd", "rock_type",
                           "rock_quality", "rock_type_advanced", "joint"]
        for property in properties:
            print(f"{property} is: {getattr(self, property)}")
