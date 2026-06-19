from typing import Union
import numpy as np



# convert psf to tsf by multiplying
PSF2TSF = 0.000446

# Atomosphere perssure to tsf by multiplying
PA2TSF =  0.9447 # 1 atm = 0.9447 tsf

# convert psi to tsf by multiplying
PSI2TSF = 0.072

# lower and upper limit of normalized tip resistance
QTN_MIN = 1.0
QTN_MAX = 1000.0

# lower and upper limit of normalized friction ratio
FR_MIN = 0.1
FR_MAX = 10.0

# lower limit of effective vertical stress in tsf
SIGMA_VO_PRIME_MIN = 0.001

# nonzero offset
NONZERO_OFFSET = 1E-14

# unit weight of water in pcf
UNIT_WEIGHT_WATER = 62.4

# scalar data type
SCALAR_TYPE = Union[int, float, np.integer, np.floating]
SCALAR_TYPES = (int, float, np.integer, np.floating)

# array data type
ARRAY_TYPE = Union[np.ndarray]
ARRAY_TYPES = (np.ndarray,)

# numeric types
NUMERIC_TYPES = SCALAR_TYPES + ARRAY_TYPES