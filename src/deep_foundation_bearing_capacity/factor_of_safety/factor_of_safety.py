# class for factor of safety

from deep_foundation_bearing_capacity.constants.constants import NUMERIC_TYPE


class FactorOfSafety:
    '''
    Class for factor of safety of general foundations, including shallow and deep foundations

    '''
    def __init__(self, factor_of_safety: NUMERIC_TYPE = 3.0):
        """
        Args:
            factor_of_safety (NUMERIC_TYPE): for shallow foundation, typically use 3.0
        """
        
        # sanity check
        self._sanity_check_fs(factor_of_safety)
        self.factor_of_safety = factor_of_safety


    def _sanity_check_fs(self, fs)-> bool:
        '''
        To perform sanity check on all factor of safety

        Args:
            fs: factor of safety
        
        Returns:
            result (bool): True or False
        '''

        if not isinstance(fs, NUMERIC_TYPE):
            raise TypeError("ERROR: fs shall be type {NUMERIC_TYPE}.")
        elif fs < 1.0:
            raise ValueError("ERROR: fs shall be not less than unity.")
        else:
            return True

class FactorOfSafetyDeepFoundation (FactorOfSafety):
    '''
    Class for deep foundations
    
    '''
    def __init__(self, factor_of_safety: NUMERIC_TYPE = 3.0, fs_end_bearing: NUMERIC_TYPE = 3.0):
        '''
        Args:
            fs (constants.SCALAR_TYPE): used for skin friction
                                        without load test (typical), use 3.0;
                                        with laod test, use 2.0 
            fs_end_bearing (constants.SCALAR_TYPE): used for end bearing
        '''
        super().__init__(factor_of_safety)

        # sanity check on fs_end bearing
        if fs_end_bearing is None:
            fs_end_bearing = self.factor_of_safety
        else:
            self._sanity_check_fs(fs_end_bearing)

        # factor of safety for deep foundation
        self.fs_deep_foundation_skin_compression = self.factor_of_safety
        self.fs_deep_foundation_skin_uplift = self.factor_of_safety
        self.fs_deep_foundation_end = fs_end_bearing


        
