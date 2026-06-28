# class for factor of safety

from deep_foundation_bearing_capacity.constants import constants


class FactorOfSafety:
    '''
    Class for factor of safety of general foundations
    
    '''
    def __init__(self, factor_of_safety):
        
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

        if not isinstance(fs, constants.SCALAR_TYPES):
            raise TypeError("ERROR: fs shall be type {constants.SCALAR_TYPES}.")
        elif fs <= 0:
            raise ValueError("ERROR: fs shall be greater than zero.")
        else:
            return True

class FactorOfSafetyDeepFoundation (FactorOfSafety):
    '''
    Class for deep foundations
    
    '''
    def __init__(self, factor_of_safety:constants.SCALAR_TYPE, fs_end_bearing:constants.SCALAR_TYPE):
        '''
        Args:
            fs (constants.SCALAR_TYPE): used for skin friction
            fs_end_bearing (constants.SCALAR_TYPE): used for end bearing
        '''
        super().__init__(factor_of_safety)

        # sanity check on fs_end bearing
        self._sanity_check_fs(fs_end_bearing)

        # factor of safety for deep foundation
        self.fs_deep_foundation_skin = self.factor_of_safety
        self.fs_deep_foundation_end = fs_end_bearing
        
