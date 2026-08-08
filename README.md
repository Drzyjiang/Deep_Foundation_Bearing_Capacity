# Deep Foundation Bearing Capacity
![CI](https://github.com/Drzyjiang/Deep_Foundation_Bearing_Capacity)
A project for calculating drilled pier geotechnical axial bearing capacity.   
Author: Zhiyan Jiang [(http://www.linkedin.com/in/zhiyanjiang)](http://www.linkedin.com/in/zhiyanjiang)

## Overview
Deep foundations such as drilled shafts are widely selected to support superstructures subject to relatively large loadings or unfavorable surficial geotechnical conditions. In designing deep foundations, geotechnical axial capacity is a crucial and potentially the governing factor in design.    
This project implements drill shafts' geotechnical axial capacity by reproducing recommended methods published by Federal Highway Administration (1999) by Python code. Altough FHWA later on pulished updated versions in 2010 and 2018, methods in the 1999 report is still considered valid in engineering practice.

## Features
### Side and end resistances in cohesive soils.
Side resistance in cohesive soil, i.e., adhesion, is denoted as the product of soil's undrained shear strength and an adhesion factor that is usually noted as $\alpha$. Thus this method is also known as the "alpha" method. Side resistance is calculated using the following equation:<br>
$$f_{max} = \alpha S_u$$
where adhesion factor $\alpha$ depends on $S_u/p_a$ ratio and varies linearly from 0.55 with $S_u/p_a$ ratio 1.5 to 0.45 with the ratio of 2.5 and remains constant beyond; $S_u$ is soil's undrained shear strength.  It is also noted that adhesion shall be neglected for upper 5 ft clayey soil or depth of seasonal moisture change, whichever is deeper, and for the shaft section $B$ (shaft diameter) above bottom.

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
Side ressitance in cohesive intermediate geomaterial (IGM) has a similar form to that for cohesive soil:
$$f_{max} = \alpha \phi q_u$$
where coefficient $\alpha$ is esimated using FHWA (1999) Figure 11.5. It has a decreasing trend with $q_u$ and an increasing trend with pressure exerted by fluid concrete. If rock's angle of interface friction deviates from 30°, $\alpha$ is factored by $\tan(\phi_{rc})/\tan30°$. Factor $\phi$ is determined by RQD and joint condition as show in the table below:
||$\phi$|$\phi$|
|:------:|:--:|:--:|
|RQD|closed joints|open gouge-filled joints| 
|100|1.00|0.85|
|70|0.85|0.55|
|50|0.60|0.55|
|30|0.50|0.50|
|20|0.45|0.45|
|<20|N/A|N/A|

End resistance in cohesive IGM is the same as in rock.

Side resistance in cohesionless IGM has a smilar form as the "beta" method, except that beta is explicitly expressed as the product of at-rest earth pressure coefficient and tangent of internal friction angle:
$$f_{max}=\sigma^\prime_{v} K_o \tan \phi^\prime$$

where at-rest earth pressure coefficient $K_o$ is calculated by:

$$k_o=(1-\sin\phi^\prime_i)[\frac {0.2p_a N_{60}} {\sigma^{\prime}_v}]^{\sin \phi^{\prime}_i}$$

Internal friction angle is calculated by:

$$\phi^{\prime} = \tan^{-1}\{[\frac {N_{60}}{12.3+20.3(\frac {\sigma^{\prime}_v}{p_a})}]^{0.34}\}$$



## Installation
```bash
# For user
pip install git+https://github.com/Drzyjiang/Deep_Foundation-_Bearing_Capacity.git
# For developer
git clone https://github.com/Drzyjiang/Deep_Foundation-_Bearing_Capacity.git
cd Deep_Foundation_Bearing_Capacity
pip install -e ".[dev]"
pytest
```

## Usage

1. Make sure dependencies are installed (See Installation).

2. Launch Jupyter Notebook:

```bash
jupyter notebook
```
3. Open notebooks\'deep_foundation_bearing_capacity_soil.ipynb' or notebooks\'deep_foundation_bearing_capacity_rock.ipynb'
and run all cells (Cell -> Run All).

4. Soil parameters and associated layer parameters are configured in 'data/soil_params.yaml' and 'data/layer_params.yaml', respsectively.
   Rock parameters and associated layer parameters are configured in 'data/rock_params.yaml' and 'data/layer_params1.yaml'.
   Edit these files to analyze a different profiles.

5. Results (bearing capacity values and plots) are displayed inline in the notebook.

6. Core calculation logic is in 'src/'; the notebook imports these modules and demonstrates usage with example cases.

## Project Structure
```bash
Deep_Foundation_Bearing_Capacity/
|---pyproject.toml			# Project configuration
|---README.md						# Documentation
+---data/               # geomaterial and layer data for notebook examples
|     |---layer_params.yaml
|     |---layer_params1.yaml
|     |---rock_params.yaml
|     |---soil_params.yaml
|     |---soil_params_clay and sand.7z # soil params backup
|     |---soil_params_cohesionless igm.7z  # cohesionless IGM params backup
+---notebooks
|     |---deep_foundation_capacity_rock.ipynb # notebook for rock strata
|     |---deep_fouddation_capacity_soil.ipynb # notebook for soil strata
|     |---nb_utilis.py                        # notebook utilities
+---src
|    +---deep_foundation_bearing_capacity/   # main package
|    |    +---constants/                 # engineering constants
|    |    |     |---__init__.py
|    |    |     |---constants.py
|    |    +---cross_sections/            # cross sections
|    |    |     |---cross_sections.py
|    |    +---geomaterials/              # geomaterial classes
|    |    |     |---__init__.py
|    |    |     |---geomaterial.py      # abstract class
|    |    |     |---layer.py
|    |    |     |---rock.py
|    |    |     |---layer.py
|    |    +---segement/
|    |    |     +---cohesive_igm/        # digitized alpha vs sigma_n data
|    |    |     |---segment.py
|    |    |     |---unit_resistance.py   # side and end unit resistance     
|    |    +---factor_of_safety/          # factor of safety
|    |    |     |---factor_of_safety.py
|    |    +---foundation/                # foundation and materials
|    |    |     |---__init__.py
|    |    |     |---deep_foundation.py
|    |    |     |---foundation_material.py
+---tests/                               # pytest suite, flattened
|     |---...
+---.github/---workflows/ci.yml          # CI


```

Key entry points:
- `deep_foundation.DeepFoundation` — construct a pile from segments
- `segments.unit_resistance` - unit resistance values

## Calculation Examples
### Example 1: soil strata
Soil parameters are below:
- soil_index: 0
  unit_weight: 120 # pcf
  friction_angle: 30 # degree
  cohesion: 0 # psf
  n60: 5

- soil_index: 1
  unit_weight: 120 
  friction_angle: 0
  cohesion: 500
  n60: 6

- soil_index: 2
  unit_weight: 115
  friction_angle: 30
  cohesion: 0
  n60: 10

- soil_index: 3
  unit_weight: 115
  friction_angle: 0
  cohesion: 2000
  n60: 6

- soil_index: 4
  unit_weight: 130
  friction_angle: 30
  cohesion: 0
  n60: 19

- soil_index: 5
  unit_weight: 130
  friction_angle: 0
  cohesion: 4000
  n60: 19

- soil_index: 6
  unit_weight: 130
  friction_angle: 30
  cohesion: 0
  n60: 26

- soil_index: 7
  unit_weight: 130
  friction_angle: 0
  cohesion: 200
  n60: 26  

- soil_index: 8
  unit_weight: 130
  friction_angle: 30
  cohesion: 0
  n60: 20

- soil_index: 9
  unit_weight: 130
  friction_angle: 0
  cohesion: 8000
  n60: 20

- soil_index: 10
  unit_weight: 115
  friction_angle: 30
  cohesion: 0
  n60: 30      

- soil_index: 11
  unit_weight: 120
  friction_angle: 0
  cohesion: 1000
  n60: 0    

Soil layer parameters are:
- layer_index: 0
  top_depth: 0
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft
  
- layer_index: 1
  top_depth: 10
  thickness: 5 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 2
  top_depth: 15
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 3
  top_depth: 25
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 4
  top_depth: 35
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 5
  top_depth: 45
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 6
  top_depth: 55
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 7
  top_depth: 65
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 8
  top_depth: 75
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 9
  top_depth: 85
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 10
  top_depth: 95
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 11
  top_depth: 105
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft
  
Ultimate compression capacity is: <br>
<img src="notebooks/soil_compression capacity.png" width="40%"> <br>

Ultimate uplift capacity is: <br>
<img src="notebooks/soil_uplift capacity.png" width="40%"> <br>

### Example 2: rock strata
Rock parameters are:
- rock_index: 0
  unit_weight: 150 # pcf
  friction_angle: 30 # degree
  qu: 10000 # psf
  rqd: 100
  rock_type: A
  rock_quality: "Excellent"
  rock_type_advanced: NULL
  joint: "open"

- rock_index: 1
  unit_weight: 150 # pcf
  friction_angle: 27 # degree
  qu: 10000 # psf
  rqd: 100
  rock_type: A
  rock_quality: "Excellent"
  rock_type_advanced: igm_cohesive
  joint: "open"

- rock_index: 2
  unit_weight: 150 # pcf
  friction_angle: 30 # degree
  qu: 10000 # psf
  rqd: 90
  rock_type: A
  rock_quality: "Very good"
  rock_type_advanced: igm_cohesive
  joint: "open"

Rock layer parameters are:
- layer_index: 0
  top_depth: 0
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft
  
- layer_index: 1
  top_depth: 10
  thickness: 5 # ft
  ground_water_depth: 15.0 # ft

- layer_index: 2
  top_depth: 15
  thickness: 10 # ft
  ground_water_depth: 15.0 # ft

Ultimate compression capacity is: <br>
<img src="notebooks/rock_compression capacity.png" width="40%"> <br>

Ultimate uplift capacity is: <br>
<img src="notebooks/rock_uplift capacity.png" width="40%"> <br>

## References
1. Federal Highway Administration. (1999). Drilled Shafts Construction Procedures and Design Methods. FHWA-IF-99-025.
