# con2020
[![image](https://zenodo.org/badge/doi/10.5281/zenodo.6959770.svg)](https://doi.org/10.5281/zenodo.6959770)

Python implementation of the Connerney et al., 1981 and Connerney et al., 2020 Jovian magnetodisc model. This model provides the magnetic field due to a "washer-shaped" current near to Jupiter's magnetic equator. This model code uses either analytical equations from Edwards et al., 2001 or the numerical integration of the Connerney et al., 1981 equations to provide the magnetodisc field, depending upon proximity to the disc along _z_ and the inner edge of the disc, _r<sub>0</sub>_.

The LASP webpage describes the [Community Code](https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2Flasp.colorado.edu%2Fmop%2Fmissions%2Fjuno%2Fcommunity-code%2F&data=05%7C01%7Cgp31%40leicester.ac.uk%7C2eb0d04b2d75428c9bd008db5c013c2c%7Caebecd6a31d44b0195ce8274afe853d9%7C0%7C0%7C638204932610327781%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=WDeAEBt9Sb3PdL%2B6ANqx3DAjQ5sGrO4YhMOig%2B8V%2BE8%3D&reserved=0), and lists all the Community Githubs.

These codes were developed by Fran Bagenal, Marty Brennan, Matt James, Gabby Provan, Aneesah Kamran,  Marissa Vogt, and Rob Wilson, with thanks to Jack Connerney and Masafumi Imai. They are intended for use by the Juno science team and other members of the planetary magnetospheres community. Our contact information is in the documentation PDF file.

In 2023, our efforts were published in [Space Science Reviews](https://link.springer.com/article/10.1007/s11214-023-00961-3) . If using these codes, please reference this SSR paper and the DOI of the particular codes.

## Installation

Install the module using `pip3`:

```bash
pip3 install --user con2020

#or if you have previously installed using this method
pip3 install --upgrade --user con2020
```

Or using this repo:

```bash
#clone the repo
git clone https://github.com/gabbyprovan/con2020
cd con2020

#EITHER create a wheel and install (X.X.X is the current version number)
python3 setup.py bdist_wheel
pip3 install --user dist/con2020-X.X.X-py3-none-any.whl

#or directly install using setup.py
python3 setup.py install --user
```

## Usage

To call the model, an object must be created first using `con2020.Model()`, where the default model parameters, model equations used or coordinate systems of input and output can be altered using keywords, e.g:

```python
import con2020

#initialize a model object with default parameters
def_model = con2020.Model()

#initialize a model which uses spherical polar coordinates for input and output
sph_model = con2020.Model(CartesianIn=False,CartesianOut=False)

#initialize a model with custom parameters (longhand)
cust_model0 = con2020.Model(mu_i_div2__current_parameter_nT=150.0,
                           	r0__inner_rj=9.5,
                           	d__cs_half_thickness_rj=3.1)

#equivalently, a custom parameter model (shorthand)
cust_model1 = con2020.Model(mu_i=150.0,r0=9.5,d=3.1)
```

Once a model object is initialized, the model field can be obtained by calling the member function `Field()` and supplying input coordinates as three scalars, or three arrays (all of which are in right-handed System III), e.g.:

```python
#Example 1: the model at a single Cartesian position (all in Rj)
x = 5.0
y = 10.0
z = 6.0
Bcart = def_model.Field(x,y,z)
Result:
Bxyz=[15.58367964 36.8963783  63.04540543] nT
Calculated using the default con2020 model keywords and the hybrid approximation.

#Example 2: the model at an array of positions of spherical polar coordinates
r = np.array([10.0,20.0])					#radial distance in Rj
theta = np.array([30.0,35.0])*np.pi/180.0	#colatitude in radians 
phi = np.array([90.0,95.0])*np.pi/180.0	#east longitude in radians
Bpol = sph_model.Field(r,theta,phi)
Result:
Spherical polar Brtp =[63.31325114 ,31.15605062], [-21.02247982 , -6.8652712], [-3.60747376, -2.72695432] nT
Cartesian       Bxyz =[3.60747376, 1.64920933], [13.450624,  12.43774298], [65.34212379, 29.45930035] nT
Calculated using the default con2020 model keywords and the hybrid approximation.
```

The output will be a `numpy.ndarray` with a shape `(n,3)`, where `n` is the number of input coordinates, `B[:,0]` corresponds to either `Bx` or `Br`; `B[:,1]` corresponds to `By` or `Btheta`; and `B[:,2]` corresponds to either `Bz` or `Bphi`.  A full list of model keywords is shown below:

| Keyword (long)                            | Keyword (short) | Default Value | Description                                                  |
| ----------------------------------------- | --------------- | ------------- | ------------------------------------------------------------ |
| `mu_i_div2__current_parameter_nT`           | `mu_i`          | `139.6`*      | Current sheet current density in nT.                         |
| `i_rho__radial_current_MA`        | `i_rho`         | `16.7`*       | <sup>†</sup>Radial current intensity in MA from Connerney et al 2020.      |
| `r0__inner_rj`                            | `r0`            | `7.8`         | Inner edge of the current sheet in R<sub>j</sub>.            |
| `r1__outer_rj`                            | `r1`            | `51.4`        | Outer edge of the current sheet in R<sub>j</sub>.            |
| `d__cs_half_thickness_rj`                 | `d`             | `3.6`         | Current sheet half thickness in R<sub>j</sub>.               |
| `xt__cs_tilt_degs`                        | `xt`            | `9.3`         | Tilt angle of the current sheet away from the SIII _z_-axis in degrees. |
| `xp__cs_rhs_azimuthal_angle_of_tilt_degs` | `xp`            | 155.8         | (Right-Handed) Longitude towards which the current sheet is tilted in degrees. |
| `equation_type`                           |                 | `'hybrid'`    | Which method to use, can be:<br />`'analytic'`  - use only the analytical equations<br />`'integral'` - numerically integrate the equations<br />`'hybrid' `- a combination of analytical and integration (default) |
| `error_check`                             |                 | `True`        | Check errors on inputs the the `Field()` member function - set to `False` at your own risk for a slight speedup. |
| `CartesianIn`                             |                 | `True`        | If `True` (default) then the input coordinates are expected to be in Cartesian right-handed SIII coordinates. If `False` then right-handed spherical polar SIII coordinates will be expected. |
| `CartesianOut`                            |                 | `True`        | If `True` the output magnetic field components will be in right-handed Cartesian SIII coordinates. If `False` then the output will be such that it has radial, meridional and azimuthal components. |
| `azfunc` | | `'connerney'` | Which model to use for the azimuthal component of the magnetodisc current: </br> `'connerney'` - use Connerney et al., 2020 model </br> `'lmic'` - use the Leicester magnetosphere-ionosphere coupling (L-MIC) model (Cowley et al., 2005, 2008). |
| `DeltaRho` | | `1.0`               | Scale length over which smoothing is done in the $\rho$ direction R<sub>J</sub>.                                                                                                                                                                     |
| `DeltaZ`  | | `0.1`                | Scale length over which smoothing is done in the $z$ direction.                                                                                                                                                                                      |
| `g`   |     | `417659.3836476442`  | <sup>§</sup>Magnetic dipole parameter, nT                                                                                                                                                                                                                      |
| `wO_open` | | `0.1`                | <sup>§</sup>Ratio of plasma to Jupiter's angular velocity on open field lines.                                                                                                                                                                                 |
| `wO_om`   | | `0.35`               | <sup>§</sup>Ratio of plasma to Jupiter's angular velocity in the outer magnetosphere.                                                                                                                                                                          |
| `thetamm` | | `16.1`               | <sup>§</sup>Colatitude of the centre of the middle magnetosphere, where the plasma transitions from corotating to sub-corotating, °.                                                                                                                           |
| `dthetamm` || `0.5`              | <sup>§</sup>Colatitude range over which the transition from inner to outer magnetosphere occurs, °.                                                                                                                                                            |
| `thetaoc`  || `10.716`            | <sup>§</sup>Colatitude of the centre of the open-closed field line boundary, °.                                                                                                                                                                                |
| `dthetaoc` || `0.125`              | <sup>§</sup>Colatitude range of the open-closed field line boundary, °.                                                                                                                                                                                        |

*Default current densities used here are averages provided in Connerney et al., 2020 (see Figure 6), but can vary from one pass to the next. Table 2 of Connerney et al., 2020 provides a list of both current densities for 23 out of the first 24 perijoves of Juno.

<sup>†</sup> This is only applicable for the Connerney et al., 2020 model for $B_{\phi}$.

<sup>§</sup> These parameters are used to configure the L-MIC model for $B_{\phi}$.

The `con2020.Test()` function should produce the following:

![](Test.png)

## References

- Connerney, J. E. P., Timmins, S., Herceg, M., & Joergensen, J. L. (2020). A Jovian magnetodisc model for the Juno era. *Journal of Geophysical Research: Space Physics*, 125, e2020JA028138. https://doi.org/10.1029/2020JA028138
- Connerney, J. E. P., Acuña, M. H., and Ness, N. F. (1981), Modeling the Jovian current sheet and inner magnetosphere, *J. Geophys. Res.*, 86( A10), 8370– 8384, doi:[10.1029/JA086iA10p08370](https://doi.org/10.1029/JA086iA10p08370).
- Cowley, S. W. H., Alexeev, I. I., Belenkaya, E. S., Bunce, E. J., Cottis, C. E., Kalegaev, V. V., Nichols, J. D., Prangé, R., and Wilson, F. J. (2005), A simple axisymmetric model of magnetosphere-ionosphere coupling currents in Jupiter's polar ionosphere, *J. Geophys. Res.*, 110, A11209, doi:[10.1029/2005JA011237](https://doi.org/10.1029/2005JA011237 "Link to external resource: 10.1029/2005JA011237").
- Cowley, S. W. H., Deason, A. J., and Bunce, E. J.: Axi-symmetric models of auroral current systems in Jupiter's magnetosphere with predictions for the Juno mission, Ann. Geophys., 26, 4051–4074, https://doi.org/10.5194/angeo-26-4051-2008, 2008.
- Edwards T.M., Bunce E.J., Cowley S.W.H. (2001), A note on the vector potential of Connerney et al.'s model of the equatorial current sheet in Jupiter's magnetosphere, *Planetary and Space Science,*49, 1115-1123,https://doi.org/10.1016/S0032-0633(00)00164-1.
