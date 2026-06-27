# method for general shallow foundation bearing capacity
import numpy as np

from src.constants import constants


class general_bearing_capacity:
    def __init__(self, shallow_foundation, layer, 
                 factor_of_safety:float = 3.0, large_foundation_correction:bool = True):
        '''
        To initialize for general bearing capacity factors 

        Args:
            shallow_foundation (shallow_foundation): shallow_foundation object
            layer (layer): layer object
        '''

        # References
        self.references = ["Principles of geotechnical engineering. 8th, Das."]


        self.shallow_foundation = shallow_foundation
        self.layer = layer

        self.large_foundation_correction = large_foundation_correction

        self.factor_of_safety = factor_of_safety

    def _calculate_Nq(self)->np.array:
        '''
        To calculate bearing capacity factor of surcharge
        
        '''

        # Extract friction angle in radians
        phi = np.atleast_1d(np.asarray(self.layer.soil.friction_angle, dtype = float))
        phi = np.radians(self.layer.soil.friction_angle)

        return np.exp(np.pi * np.tan(phi)) * np.square(np.tan(np.radians(45) + phi / 2.0))
    
    def _calculate_Nc(self)->np.array:
        '''
        To calculate bearing capacity factor of cohesion
        '''
        # Extract friction angle in radians
        phi = np.atleast_1d(np.asarray(self.layer.soil.friction_angle, dtype=float))
        phi = np.radians(self.layer.soil.friction_angle)

        nq = self._calculate_Nq()

        '''
        if phi > 0: # cohesionless
            return np.array([(nq - 1) * 1.0/np.tan(phi)])
        else: # cohesive
            return np.array([5.14])
        '''

        nc = np.zeros(phi.shape)
        nc[phi == 0] = 5.14
        nc[phi >0] = (nq[phi>0] - 1) * 1.0/np.tan(phi[phi>0])

        return nc        
        
    
    def _calculate_Nr(self):
        '''
        To calculate bearing capacity factor of self weight
        '''

        # Extract friction angle in radians
        phi = np.atleast_1d(np.asarray(self.layer.soil.friction_angle, dtype = float))
        phi = np.radians([self.layer.soil.friction_angle])

        nq = self._calculate_Nq()

        return 2*(nq + 1) *np.tan(phi)
    
    def _test_Nq(self, epsilon = 0.01)->bool:
        '''
        To test correctness of _calculate_Nq

        Args:
            epsilon (float): tolerance of relative difference.
                             e.g., 0.02 means 2%
        Returns:
            validate (bool): True if benchmark test pass,
                             False if fails 
        '''

        # extract 
        friction_angle_for_test = self._bearing_capacity_factor_benchmark()[:, 0]

        nq_benchmark = self._bearing_capacity_factor_benchmark()[:, 2]

        # get decimal length
        decimal_length = len(str(nq_benchmark[-1]).split('.')[1])

        # backup friction angle
        friction_angle_backup = self.layer.soil.friction_angle

        # modify friction angle
        self.layer.soil.modify_friction_angle(friction_angle_for_test)
        #self.layer.soil.friction_angle = friction_angle_for_test

        nq_calculated = np.round(self._calculate_Nq(), decimal_length)

        # compare
        validate =  np.max(np.abs((nq_calculated - nq_benchmark) /
                                  (nq_benchmark + constants.NONZERO_OFFSET) ) <= epsilon)

        # restore friction angle
        self.layer.soil.friction_angle = friction_angle_backup

        return validate
    
    def _test_Nc(self, epsilon = 0.01)->bool:
        '''
        To test correctness of _calculate_Nc

        Args:
            epsilon (float): tolerance of difference
                            e.g., 0.02 means 2%
        Returns:
            validate (bool): True if benchmark test pass,
                             False if fails 
        '''
        friction_angle_for_test = self._bearing_capacity_factor_benchmark()[:, 0]

        nc_benchmark = self._bearing_capacity_factor_benchmark()[:, 1]

        # get decimal length
        decimal_length = len(str(nc_benchmark[-1]).split('.')[1])

        # backup friction angle
        friction_angle_backup = self.layer.soil.friction_angle

        # modify friction angle
        self.layer.soil.friction_angle = friction_angle_for_test

        nc_calculated = np.round(self._calculate_Nc(), decimal_length)

        # compare
        validate =  np.max(np.abs((nc_calculated - nc_benchmark) /
                                  (nc_benchmark + constants.NONZERO_OFFSET) ) <= epsilon)

        # restore friction angle
        self.layer.soil.friction_angle = friction_angle_backup

        return validate
    
    def _test_Nr(self, epsilon = 0.01)->bool:
        '''
        To test correctness of _calculate_Nr

        Args:
            epsilon (float): tolerance of difference
        Returns:
            validate (bool): True if benchmark test pass,
                             False if fails 
        '''
        friction_angle_for_test = self._bearing_capacity_factor_benchmark()[:, 0]

        nr_benchmark = self._bearing_capacity_factor_benchmark()[:, 3]

        # get decimal length
        decimal_length = len(str(nr_benchmark[-1]).split('.')[1])

        # backup friction angle
        friction_angle_backup = self.layer.soil.friction_angle

        # modify friction angle
        self.layer.soil.friction_angle = friction_angle_for_test

        nr_calculated = np.round(self._calculate_Nr(), decimal_length)
   
        # compare
        validate =  np.max(np.abs((nr_calculated - nr_benchmark) /
                                  (nr_benchmark + constants.NONZERO_OFFSET) ) <= epsilon)

        # restore friction angle
        self.layer.soil.friction_angle = friction_angle_backup

        return validate


    
    def _bearing_capacity_factor_benchmark(self)->np.array:
        '''
        To hard code Nc values for verification

        Returns:
            nc_values (np.array): first column is effective friction angle in unit of degree, 
                                  second column is Nc, third column is Nq, last column is Nr
        '''
        bearing_capacity_factors = np.array([[ 0, 5.14, 1.00, 0.00],
                              [ 1,  5.38,   1.09,   0.07],
                              [ 2,  5.63,   1.20,   0.15],
                              [ 3,  5.90,   1.31,   0.24],
                              [ 4,  6.19,   1.43,   0.34],
                              [ 5,  6.49,   1.57,   0.45],
                              [ 6,  6.81,   1.72,   0.57],
                              [ 7,  7.16,   1.88,   0.71],
                              [ 8,  7.53,   2.06,   0.86],
                              [ 9,  7.92,   2.25,   1.03],
                              [10,  8.35,   2.47,   1.22],
                              [11,  8.80,   2.71,   1.44],
                              [12,  9.28,   2.97,   1.69],
                              [13,  9.81,   3.26,   1.97],
                              [14, 10.37,   3.59,   2.29],
                              [15, 10.98,   3.94,   2.65],
                              [16, 11.63,   4.34,   3.06],
                              [17, 12.34,   4.77,   3.53],
                              [18, 13.10,   5.26,   4.97],
                              [19, 13.93,   5.80,   4.68],
                              [20, 14.83,   6.40,   5.39],
                              [21, 15.82,   7.07,   6.20],
                              [22, 16.88,   7.82,   7.13],
                              [23, 18.05,   8.66,   8.20],
                              [24, 19.32,   9.60,   9.44],
                              [25, 20.72,  10.66,  10.88],
                              [26, 22.25,  11.85,  12.54],
                              [27, 23.94,  13.20,  14.47],
                              [28, 25.80,  14.72,  16.72],
                              [29, 27.86,  16.44,  19.34],
                              [30, 30.14,  18.40,  22.40],
                              [31, 32.67,  20.63,  25.99],
                              [32, 35.49,  23.18,  30.22],
                              [33, 38.64,  26.09,  35.19],
                              [34, 42.16,  29.44,  41.06],
                              [35, 46.12,  33.30,  48.03],
                              [36, 50.59,  37.75,  56.31],
                              [37, 55.63,  42.92,  66.19],
                              [38, 61.35,  48.93,  78.03],
                              [39, 67.87,  55.96,  92.25],
                              [40, 75.31,  64.20, 109.41],
                              [41, 83.86,  73.90, 130.22],
                              [42, 93.71,  85.38, 155.55],
                              [43,105.11,  99.02, 186.54],
                              [44,118.37,  115.31,224.64],
                              [45,133.88,  134.88,271.76],
                              [46,152.10,  158.51,330.35],
                              [47,173.64,  187.21,403.67],
                              [48,199.26,  222.31,496.01],
                              [49,229.93,  265.51,613.16],
                              [50,266.89,  319.07,762.89]
                              ])
        
        return bearing_capacity_factors





            