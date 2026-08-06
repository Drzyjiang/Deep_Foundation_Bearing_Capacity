# Deep Foundation Bearing Capacity
![CI](https://github.com/Drzyjiang/Deep_Foundation_Bearing_Capacity)
A project for calculating deep foundation ultimate bearing capacity. Phase I includes geotechnical axial bearing capacity of drilled piers.  
Author: Zhiyan Jiang [(http://www.linkedin.com/in/zhiyanjiang)](http://www.linkedin.com/in/zhiyanjiang)


## Overview
Deep foundations such as drilled shafts are widely adopted to support superstructures that subject to relatively large loadings or located at areas with unfavorable surficial geotechnical conditions. In designing deep foundations, engineers typically need to analyze geotechncial and structural capacities in axial and lateral directions.   
This project implements Python code for calculating drill shafts' geotechnical axial capacity by reproducing recommended methods published by Federal Highway Administration (1999).

## Features
### Side and end resistances in cohesive soils.
Side resistance in cohesive soil, i.e., adhesion, is determined by undrained shear strength and an adhesion factor that is usually denoted as alpha. Thus this method is also called the "alpha" method. Side resistance is calculated using the following equation:
$$f_{max} = \alpha S_u$$
where adhesion factor $\alpha$ depends on $S_u/p_a$ ratio and varies linearly from 0.55 with $S_u/p_a$ ratio 1.5 to 0.45 with the ratio of 2.5. $\alpha$ remains constant for $S_u/p_a$ ratio beyond this range; $S_u$ is soil's design undrained shear strength.  It is also noted that adhesion shall be neglected for upper 5 ft soil or depth of seasonal moisture change, whichever is deeper, and for shaft section within $B$ (shaft diameter) distance above shaft bottom.

End resistance in cohesive soil is calcualted using the equation below when depth of shafts is greater than $3B$:
$$q_{max} = N^c_* S_u$$
where $N^c_*$ is a function of rigidity index and can be interpolated by $S_u$ as below:

|$S_u$ (psf)|$N^c_*$|
|:----------:|:-----:|
|500|6.5|
|1000|8.0|
|2000|9.0|

In case of embedment less than $3B$, a factor of $\frac {2}{3} [1+\frac {1}{6}\frac{D}{B}]$ is applied.

### Side and end resistances in cohesionless soils
Side resistance in cohesionless soil is equal to factored effective normal stress applied on foundations. With effective normal stress being a function of vertical effective stress, a single dimensionless correlation factor "beta" is applied to vertical effective stress to yield side resistance:

$$f_{max} = \beta \sigma^\prime _{v}$$

where beta can be determined by standard penetration test blowcounts $N_{60}$ and depth. 
For sand,
$$ \beta = \frac {N_{60}} {15}(1.5-0.135 z^{0.5})$$ 

where $z$ is depth in unit of foot and $N_{60}$ is capped at 15. This equation also applies to gravelly sand or gravels with $N_{60} \le 15$.
For gravelly sand or gravels with $N_{60} \le 15$, the follow equation applies:
$$ \beta = 2.0-0.06 z^{0.75}$$ 

Coefficient $\beta$ is limited between 0.25 and 1.20 for sand, and between 0.25 and 1.80 for gravelly sand and gravels. Note that the thickness of each cohesionless layer is limited to 30 ft.

End resistance in sand is correlated to $N_{60}$as:
$$q_{max}= 0.60 N_{60} \le 30$$
where $q_{max}$ is in unit of ton per square foot.


### Side and end resistances in rocks
Once a drilled pier is socketed in a rock layer, its side resistance depends on the socket's roughness. For conservative design, rock socket is always assumed as smooth and the side unit resistance is computed as:

$$f_{max} = 0.65 p_a[q_u/p_a]^{0.5}$$
where $q_u$ is the smaller of rock unconfined compressive strength and 28-day compressive strength of the concrete material. 

End resistance in rock is determined by not only unconfined compressive strength, but also rock quality designation (RQD), socket depth, and joint conditions.
If RQD is 100% and socket depth is greater than 1.5 times shaft's diameter, the following equation applies:
$$q_{max} = 2.5 q_u$$
where q_u is rock's unconfined compressive strength. 
If the above conditions are not met, but RQD is above 70% and joints are horizontal closed joints, then the following equation applies:
$$q_{max} = 4.83 [q_u]^{0.51}$$
where $q_u$ and q_{max} are in unit of MPa.
If neither conditions are met, side resistance needs to be evaluated based on rock type and quality of rock mass:
$$q_{max} = [s^{0.5} + (ms^{0.5}+s)^{0.5}]q_u$$
where parameters $s$ and $m$ can be determined using FHWA (1999) Table 11.3   

### Side and end resistances in cohesive and cohesionless intermediate geomaterials
Side ressitance in cohesive intermediate geomaterial (cohesive IGM) has a similar form to that for cohesive soil:
$$f_{max} = \alpha \phi q_u$$
where \

$$q_{ult} = q_{ult,upper}\ \ \ \ (h >= 2B)$$


$$q_{ult} = 0.5 q_{ult,upper} + 0.5 q_{ult,lower}$$


$$q_{ult} = q_{ult,upper}$$


$$q_{ult}=[q_2 + \frac {1}{K}c_1 \cot(\phi_1)] \exp(2 (1+ \frac {B}{L}) K \tan(\phi_1) \frac {H} {B})- \frac {1}{K} c_1 \cot(\phi_1)$$

where $K=(1-sin^2\phi_1)/(1+sin^2\phi_1)$ and $q_2=q_{ult}\ of\ the\ same\ foundation\ but\ seated\ on\ top\ of\ the\ lower\ layer$

The calculated bearing capacity above shall not exceed the value of the upper layer:

$$q_{ult}\leq q_{ult,upper}$$


$$q_{ult}=c_1 N_m + q$$

where $c_1$ is the undrained shear strength of the upper layer. $N_m$ is a modified bearing capacity factor. Its value depends on which layer is stiffer. 
For a soft layer over a stiff layer:

$$N_{m}=\frac {\kappa N_{\ast}(N_{\ast}+\beta -1)[(\kappa +1) N_{\ast} + (1+\kappa \beta) N_{\ast} + \beta -1]} {[\kappa (\kappa +1) N_{\ast} + \kappa +\beta -1][(N_{\ast}+\beta) N_{\ast}+\beta -1]-[(\kappa N_{\ast}+\beta -1)(N_{\ast}+1)]}$$

where $\kappa=c_2/c_1$ is the relative strength, $\beta =BL/[2H (B+L)]$ is the punching index,and $N_{*}=\zeta_{cs}N_c$.

For a stiff layer over a soft layer:

$$N_m=\frac {1} {\beta}+\kappa*\zeta_{cs}N_c\ \ \ \ \ (for\ N_m\leq \zeta_{cs}*N_c)$$

## Installation
```bash
# For user
pip install git+https://github.com/Drzyjiang/Shallow_Foundation_Bearing_Capacity_Vesic.git
# For developer
git clone https://github.com/Drzyjiang/Shallow_Foundation_Bearing_Capacity_Vesic.git
cd Shallow_Foundation_Bearing_Capacity_Vesic
pip install -e ".[dev]"
pytest
```

## Usage

1. Make sure dependencies are installed (See Installation).

2. Launch Jupyter Notebook:

```bash
jupyter notebook
```
3. Open 'Shallow_Foundation_Bearing_Capacity_Vesic.ipynb' and run all cells (Cell -> Run All).

4. Soil parameters are configured in 'data/soil_params.yaml'.
   Layer parameters are configured in 'data/layer_params.yaml'.
   Shallow foundation parameters are configured in 'data/shallow_foundation_params.yaml'.
   Edit these files to analyze a different site.

5. Results (bearing capacity values and plots) are displayed inline in the notebook.

6. Core calculation logic is in 'src/'; the notebook imports these modules and demonstrates usage with example cases.

## Project Structure
```bash
Shallow_Foundation_Bearing_Capacity_Vesic/
|---pyproject.toml										# Project configuration
|---README.md											# Documentation
|---Shallow_Foundation_Bearing_Capacity_Vesic.ipynb		# Main demonstration notebook
|   
+---.github/---workflows/ci.yml
|           
+---data/												# Example input parameters
|    +---layer_params.yaml
|    |---shallow_foundation_params.yaml
|    |---soil_params.yaml
|       
+---results												# Example output figures
|       
+---src   
|   +---shallow_foundation_bearing_capacity 			# Main package
|   |   +---bearing_capacity    						# Capacity algorithms
|   |   +---constants      								# Physical constants
|   |   +---foundation      							# Foundation geometry models
|   |   +---soil_layer									# Soil and layer parameters
|           
+---tests												# pytest test suite


```

## Calculation Example
Two sets of soil parameters are below:
- unit_weight: 120 # pcf 
  friction_angle: 30 # degree
  cohesion: 0 # psf 

- unit_weight: 120 
  friction_angle: 0 
  cohesion: 2000

Ultimate bearing capacity of the upper layer by the single-layer model is: <br>
<img src="results/single_layer_model_results.png" width="40%"> <br>

Ultimate bearing capacity of by the two-layer model is: <br>
<img src="results/two_layer_model_results.png" width="40%"> <br>

## References
1. Electric Power Research Institute. Transmission Line Structure Foundations for Uplift-Compression Loading. EL-2870 Report, 1983.
2. US Army Corps of Engineers. Engineering and Design Bearing Capacity of Soils. EM 1110-1-1905, 1992.
3. Bowles, J.B. Foundation Analysis and Design. Fifth Ed. McGraw-Hill, 1996. 
4. Meyerhof, G. G. (1974). Ultimate bearing capacity of footings on sand layer overlying clay. Canadian Geotechnical Journal, 11(2), 223–229. https://doi.org/10.1139/t74-018
5. Meyerhof, G. G., & Hanna, A. M. (1978). Ultimate bearing capacity of foundations on layered soils under inclined load. Canadian Geotechnical Journal, 15(4), 565–572.
6. Vesić, A. S. (1975). Bearing capacity of shallow foundations. In H. F. Winterkorn & H. Y. Fang (Eds.), Foundation Engineering Handbook (1st ed., Chapter 3, pp. 121–147). Van Nostrand Reinhold, New York.