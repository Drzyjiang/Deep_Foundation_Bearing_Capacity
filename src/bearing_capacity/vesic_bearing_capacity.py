# method for Vesic shallow foundation bearing capacity

import numpy as np
from typing import Union, overload
import copy

from src.bearing_capacity.general_bearing_capacity import general_bearing_capacity
from src.foundation.shallow_foundation import ShallowFoundation
from src.constants import constants

class vesic_bearing_capacity (general_bearing_capacity):
    '''
    To calculate bearing capacity based on Vesic's method

    Notes: 
    Following critical bearing capacity factors are implemented:
    zeta_cs, zeta_cd
    zeta_gamma_s, zeta_gamma_d
    zeta_qs, zeta_qd
    gamma_r

    Following trivial bearing capacity factors are NOT implemented:
    zeta_cr, zeta_ci, zeta_ct, zeta_cg
    zeta_gamma_r, zeta_gamma_i, zeta_gamma_t, zeta_gamma_g
    zeta_qr, zeta_qi, zeta_qt, zeta_qg
    
    '''
    def __init__(self, shallow_foundation, layer, factor_of_safety = 3.0, large_foundation_correction:bool = True, adjustment_to_depth = 0):
        super().__init__(shallow_foundation, layer, factor_of_safety, large_foundation_correction)

        self._sanity_check_adjustment_to_depth(adjustment_to_depth)

        self._references = ["EPRI: EL-2870 Transmission Line Structure Foundations for Uplift Compression Loading. Chapter 7"]

        # foundation width
        self.b = self.shallow_foundation.foundation_width

        # foundation length
        self.l = self.shallow_foundation.foundation_length

        # calculation depth
        self.d = self.shallow_foundation.foundation_embedment + adjustment_to_depth

        # friction angle
        self.phi = np.radians([self.layer.soil.friction_angle])

        # effective unit weight
        self.r_prime = self._calculate_r_prime()

    def _sanity_check_adjustment_to_depth(self, adjustment_to_depth)->bool:
        '''
        To perform sanity check on adjustment_to_depth
        '''   

        if not isinstance(adjustment_to_depth, constants.SCALAR_TYPES):
            raise TypeError(f"adjustment_to_depth shall be {constants.SCALAR_TYPE}.")
        
        return True

    
    def _calculate_zeta_cs(self):
        '''
        To calculate foundation shape factor zeta_cs 
        '''
        nq = self._calculate_Nq()
        nc = self._calculate_Nc()

        return 1+ (self.b/self.l) *(nq/nc)

    def _calculate_zeta_qs(self):
        '''
        To calculate foundation shape factor zeta_qs
        
        '''
        b = self.shallow_foundation.foundation_width
        l = self.shallow_foundation.foundation_length       

        return 1 + (self.b/self.l) * np.tan(self.phi)
    
    def _calculate_zeta_rs(self):
        '''
        To calculate foundation shape factor zeta_rs
        
        '''

        return 1 - 0.4 * (self.b/self.l)
    
    def _calculate_zeta_qd(self):
        '''
        To calculate foundation depth factor zeta_rs
        '''        

        return 1 + 2 * np.tan(self.phi) * np.square(1-np.sin(self.phi)) * np.arctan(self.d/self.b) 
    
    def _calculate_zeta_rd(self):
        '''
        To calculate foundation depth factor zeta_rd
        '''
        return np.ones(np.asarray(self.b).shape)
    
    def _calculate_zeta_cd(self):
        '''
        To calculate foundation depth factor zeta_cd
        '''
        zeta_qd = self._calculate_zeta_qd()
        nc = self._calculate_Nc()

        if self.phi > 0:
            return zeta_qd - (1 - zeta_qd) / (self._calculate_Nc() * np.tan(self.phi))
        else:
            return 1 + 0.33 * np.arctan(self.d / self.b)
        
    def _calculate_gamma_r(self):
        '''
        To calculate correction to large foundations, gamma_r
        
        references = ["Bowles, J.E. (1996) Foundation Analysis and Design, 5th Edition. Page 230",
                     "EM 1110-1 1905 Bearing Capacity of Soils. Page 4-14"]
        '''
  

        self._large_foundation_width = 6.0

        correction_to_large_foundation = self.large_foundation_correction and self.b > self._large_foundation_width

        # reference k for English unit (ft) is 6.0
        # reference k for SI unit is 2.0
        k = 6  
        gamma_r = 1 - 0.25 * np.log10(self.b / k) * correction_to_large_foundation

        return gamma_r
    
    def _calculate_r_prime(self):
        '''
        To calculate effective unit weight

        '''
        # must use effective soil unit weight
        r_total = self.layer.soil.unit_weight

        if self.layer.ground_water_depth >= self.shallow_foundation.foundation_embedment + self.shallow_foundation.foundation_width:  # no impact from GWT at all
            r_prime = r_total
        elif self.layer.ground_water_depth <= self.shallow_foundation.foundation_embedment: # full impact from GWT
            r_prime = (r_total - constants.UNIT_WEIGHT_WATER)
        else: # GWT is between foundation embedment and embedment + width. Use interpolation 
            slope = constants.UNIT_WEIGHT_WATER / self.shallow_foundation.foundation_width

            r_prime = (r_total - constants.UNIT_WEIGHT_WATER + slope * (self.layer.ground_water_depth - self.shallow_foundation.foundation_embedment))
 
        return r_prime
    
    def _calculate_surcharge(self):
        '''
        To calculate surcharge q
        '''
        # q depends on foundation_embedment vs gwt
        if self.shallow_foundation.foundation_embedment <= self.layer.ground_water_depth :
            q = self.shallow_foundation.foundation_embedment * self.layer.soil.unit_weight
        else: 
            q = self.shallow_foundation.foundation_embedment * self.layer.soil.unit_weight + \
                (self.layer.ground_water_depth - self.shallow_foundation.foundation_embedment) * (self.layer.soil.unit_weight - constants.UNIT_WEIGHT_WATER)

        return q
        
    def calculate_bearing_capacity_ultimate(self):
        '''
        To calculate ultimate bearing capacity by Vesic
        '''

        nc = self._calculate_Nc()
        nr = self._calculate_Nr()
        nq = self._calculate_Nq()

        zeta_cs = self._calculate_zeta_cs()
        zeta_rs = self._calculate_zeta_rs()
        zeta_qs = self._calculate_zeta_qs()

        zeta_cd = self._calculate_zeta_cd()
        zeta_rd = self._calculate_zeta_rd()
        zeta_qd = self._calculate_zeta_qd()

        c = self.layer.soil.cohesion
        b = self.b

        r_total = self.layer.soil.unit_weight

        gamma_r = self._calculate_gamma_r()

        
        q = self._calculate_surcharge()

        return c * nc * zeta_cs * zeta_cd + 0.5 * b * self.r_prime * nr * zeta_rs * zeta_rd * gamma_r + q * nq * zeta_qs * zeta_qd
    
    def calculate_bearing_capacity_allowable(self):
        '''
        To calculate allowable bearing capacity by Vesic

        Returns:
            allowable_bearing_capacity (np.array): allowable bearing capacity
        '''

        ultimate_bearing_capacity = self.calculate_bearing_capacity_ultimate()
        allowable_bearing_capacity = ultimate_bearing_capacity / self.factor_of_safety
        
        return allowable_bearing_capacity  
    
class vesic_bearing_capacity_layered:
    '''
    To use vesic method for two-layer model

    Case 1: adjustment to depth (self.f) >= foundation width
    Case 2: cohesionless over cohesionless
    Case 3: cohesive over cohesionless
    
    '''
    def __init__(self, bearing_capacity_upper_obj: vesic_bearing_capacity, bearing_capacity_lower_obj: vesic_bearing_capacity, foundation:ShallowFoundation):
        
        #
        self.bearing_capacity_upper_obj = bearing_capacity_upper_obj
        self.bearing_capacity_lower_obj = bearing_capacity_lower_obj 

        # derive bearing capacity
        self.bearing_capacity_upper_val = bearing_capacity_upper_obj.calculate_bearing_capacity_ultimate()
        self.bearing_capacity_lower_val = bearing_capacity_lower_obj.calculate_bearing_capacity_ultimate()

        # get foundation width
        self.b = bearing_capacity_upper_obj.b

        # get foundation length
        self.l = bearing_capacity_upper_obj.l

        # get distance to lower layer
        self.h = bearing_capacity_upper_obj.layer.top_depth + bearing_capacity_upper_obj.layer.thickness -\
                 bearing_capacity_upper_obj.shallow_foundation.foundation_embedment

        # Sanity check
        if bearing_capacity_upper_obj.b != bearing_capacity_lower_obj.b:
            raise ValueError("ERROR: foundation width of upper and lower layers shall be the same.")

        if bearing_capacity_upper_obj.l != bearing_capacity_lower_obj.l:
            raise ValueError("ERROR: foundation length of upper and lower layers shall be the same.")
        
        # For each layer, at least friction angle or cohesion must be zero
        if bearing_capacity_upper_obj.layer.soil.friction_angle * bearing_capacity_upper_obj.layer.soil.cohesion != 0:
            raise ValueError("ERROR: Upper layer's friction angle or cohesion must be zero.")
        
        if bearing_capacity_lower_obj.layer.soil.friction_angle * bearing_capacity_lower_obj.layer.soil.cohesion != 0:
            raise ValueError("ERROR: Lower layer's friction angle or cohesion must be zero.")

    def _determine_case(self)->int:
        '''
        Based on soil type of upper and lower layers, determine which case to apply
        '''

        if self.bearing_capacity_upper_obj.layer.soil.cohesion !=0 and \
             self.bearing_capacity_lower_obj.layer.soil.cohesion !=0: # cohesive over cohesive
            return 5
        elif self.h >= 2.0 * self.b: # influence one is two times foundation width
            return 1
        elif self.bearing_capacity_upper_obj.layer.soil.friction_angle != 0 and \
             self.bearing_capacity_lower_obj.layer.soil.friction_angle != 0: # cohesionless over cohesionless
            return 2
        elif self.bearing_capacity_upper_obj.layer.soil.friction_angle  == 0 and \
             self.bearing_capacity_lower_obj.layer.soil.cohesion == 0: # cohesive over cohesionless
            return 3
        elif self.bearing_capacity_upper_obj.layer.soil.friction_angle  != 0 and \
             self.bearing_capacity_lower_obj.layer.soil.cohesion != 0: # coheionless over cohesive
            return 4
        else:
            return -1
        
    def _calculate_kappa(self):
        '''
        To calculate relative strength kappa
        '''
        kappa = self.bearing_capacity_lower_obj.layer.soil.cohesion / self.bearing_capacity_upper_obj.layer.soil.cohesion

        return kappa
        
    def _calculate_beta(self):
        '''
        To calculate punching index beta
        '''
        return self.b * self.l / (2.0 * self.h * (self.b + self.l))

    def _calculate_Nstar(self):
        '''
        To calculate N_star = zeta_cs * Nc
        '''

        zeta_cs = self.bearing_capacity_upper_obj._calculate_zeta_cs()
        nc = self.bearing_capacity_upper_obj._calculate_Nc()

        return zeta_cs * nc

    def _calculate_Nm(self):
        '''
        To calculate modified bearing capacity factor Nm
        References: self.references[0] equation 7-59 and 7-60
        '''

        # calculate kappa
        kappa = self._calculate_kappa()

        # calculate beta
        beta = self._calculate_beta()

        # calculate nstar
        nstar = self._calculate_Nstar()

        # calculate Nc
        nc = self.bearing_capacity_upper_obj._calculate_Nc()

        # calculate zeta_cs
        zeta_cs = self.bearing_capacity_upper_obj._calculate_zeta_cs()
       

        if kappa >= 1: # c2 >= c1, soft over stiff
            nominator = kappa * nstar * (nstar + beta - 1)*((kappa+1)*np.square(nstar) + (1+kappa*beta)*nstar + beta-1)
            denominator = (kappa*(kappa+1)*nstar + kappa + beta -1) * ((nstar+beta)*nstar + beta -1) - (kappa*nstar+beta-1)*(nstar+1)
            nm = nominator / denominator
        else: # stiff over soft
            nm = 1.0/beta + kappa * zeta_cs * nc
            nm = min([nm, zeta_cs * nc])
        
        return nm


    def _calculate_k(self):
        '''
        To calculate k, which is defined as Equation 7-61 in self._references[0]
        '''
        upper_friction_angle = self.bearing_capacity_upper_obj.layer.soil.friction_angle

        k = (1 - np.square(np.sin(np.radians(upper_friction_angle)))) / (1 + np.square(np.sin(np.radians(upper_friction_angle))))

        return k

    def _calculate_case_1(self): # distance_to_lower is equal or greater than foundation width
        '''
        To calculate for the case when distance to lower layer is greater than two times the foundation width
        '''
        return self.bearing_capacity_upper_val
    
    def _calculate_case_2(self): # cohesionless over cohesionless
        '''
        To calculate for the case of a cohesionless layer over a cohesionless layer
        '''
        return 0.5 * self.bearing_capacity_upper_val + 0.5 * self.bearing_capacity_lower_val
    
    def _calculate_case_3(self): # cohesive over coheionless
        '''
        To calculate for the case of a cohesive layer over a cohesionless layer
        '''

        return self.bearing_capacity_upper_val

    def _calculate_case_4(self): # coheionless over cohesive
        '''
        To calculate for the case of cohesionless layer over a cohesive layer
        '''
        k = self._calculate_k()

        upper_friction_angle = self.bearing_capacity_upper_obj.layer.soil.friction_angle
        upper_cohesion = 0

        # need to update self.bearing_capacity_lower_val, by assuming foundation is seated on top of the lower layer, 
        # i.e., foundation_embedment = foundation_embedment + self.h

        bearing_capacity_lower_obj_update = copy.deepcopy(self.bearing_capacity_lower_obj)
        bearing_capacity_lower_obj_update.shallow_foundation.foundation_embedment = bearing_capacity_lower_obj_update.shallow_foundation.foundation_embedment +\
                                                                                       self.h
        
        bearing_capacity_lower_val_update = bearing_capacity_lower_obj_update.calculate_bearing_capacity_ultimate()

        temp = (bearing_capacity_lower_val_update + (1.0/k)* upper_cohesion * (1.0 / np.tan(np.radians(upper_friction_angle)))) * \
              np.exp(2*(1+self.b/self.l) * k * np.tan(np.radians(upper_friction_angle)) * self.h/self.b) - (1/k) * upper_cohesion *(1/np.tan(np.radians(upper_friction_angle)))

        return min([self.bearing_capacity_upper_val, temp])
    
    def _calculate_case_5(self): # cohesive over cohesive
        '''
        To calculate for the case of cohesive over cohesive
        Reference: self._references[0] page 
        '''
        c1 = self.bearing_capacity_upper_obj.layer.soil.cohesion

        # surcharge
        q = self.bearing_capacity_upper_obj._calculate_surcharge()

        # calculate Nm
        nm = self._calculate_Nm()

        return c1 * nm + q


    def calculate_bearing_capacity_ultimate(self):
        '''
        Top wrapper of calculatinig ultimate bearing capacity using the two-layer model
        '''

        # determine case number
        case_number = self._determine_case()

        if case_number == 1:
            return self._calculate_case_1()
        elif case_number == 2:
            return self._calculate_case_2()
        elif case_number == 3:
            return self._calculate_case_3()
        elif case_number == 4:
            return self._calculate_case_4()   
        elif case_number == 5:
            return self._calculate_case_5()        
        else:
            raise ValueError("ERROR: case number is undefined.")