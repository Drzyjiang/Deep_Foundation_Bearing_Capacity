# class for shallow foundation
import numpy as np

from src.constants import constants

class ShallowFoundation:
    def __init__(self, foundation_width: float, foundation_length:float, foundation_embedment: float):
        '''
        To initialize foundation class

        Args:
            foundation_width (float): foundation width in unit of foot
            foundation_length (float): foundation length in unit of foot
            foundation_embedment (float): foundation embedment in unit of foot
        
        '''

        self._sanity_check_foundation_width(foundation_width)
        self._sanity_check_foundation_length(foundation_length)
        self._sanity_check_foundation_embedment(foundation_embedment)

        self.foundation_width = foundation_width
        self.foundation_length = foundation_length
        self.foundation_embedment = foundation_embedment

        
    def _sanity_check_foundation_width(self, foundation_width):
        '''
        To perform sanity check on foundation_width

        Args:
            foundation_width: foundation width in unit of foot
        
        Returns:
            True or False 
        '''

        if not isinstance(foundation_width, constants.NUMERIC_TYPES):
            raise TypeError("ERROR: foundation_width shall be float.")
        
        if np.min(np.asarray(foundation_width)) <= 0:
            raise ValueError(f"ERROR: minimum foundation width shall be greater than zero.")
        
        
        return True
    

    
    def _sanity_check_foundation_length(self, foundation_length):
        '''
        To perform sanity check on foundation_length

        Args:
            foundation_length: foundation length in unit of foot
        
        Returns:
            True or False 
        '''

        # sanity check: neither foundation width nor foundation length can be zero

        
        if not isinstance(foundation_length, constants.NUMERIC_TYPES):
            raise TypeError("ERROR: foundation_length shall be float.")
    
        if np.min(np.asarray(foundation_length)) <= 0:
            raise ValueError(f"ERROR: minimum foundation length shall be greater than zero.")
        
        return True

    def _sanity_check_foundation_embedment(self, foundation_embedment):
        '''
        To perform sanity check on foundation_length

        Args:
            foundation_embedment: foundation length in unit of foot
        
        Returns:
            True or False 
        '''

        # sanity check: neither foundation width nor foundation length can be zero

        
        if not isinstance(foundation_embedment, constants.NUMERIC_TYPES):
            raise TypeError("ERROR: foundation_embedment shall be float.")
    
        if np.min(np.asarray(foundation_embedment)) <= 0:
            raise ValueError(f"ERROR: minimum foundation length shall be greater than zero.")
        
        return True
