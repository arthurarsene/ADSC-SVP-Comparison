# A robust framework for comparing Lagrangian and gridded Eulerian velocity fields: an example application to surface drifters and altimetry-derived surface currents

[![DOI](https://zenodo.org/badge/572132011.svg)](https://zenodo.org/badge/latestdoi/572132011)

[Arthur Coquereau and Nicholas P. Foukal (preprint, 2022)](https://egusphere.copernicus.org/preprints/2022/egusphere-2022-1450/)

[Arthur Coquereau and Nicholas P. Foukal (final paper, 2023)](https://doi.org/10.5194/os-19-1393-2023)

## Table of contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Download data](#download)
    1. [Geostrophy data set](#geostrophy)
    2. [Geostrophy+Ekman data set](#geostrophy_ekman)
    3. [Global Drifter Program (GDP) trajectories data set](#gdp)
    4. [Bathymetry Data](#bathy)
4. [3-step methodology notebooks](#methodology)


## Introduction<a name="introduction"></a>

This repository presents Python notebooks demonstrating how to apply the methodology described in [Coquereau and Foukal (preprint, 2022)](https://egusphere.copernicus.org/preprints/2022/egusphere-2022-1450/) and in [Coquereau and Foukal (final paper, 2023)](https://doi.org/10.5194/os-19-1393-2023). This 3-step methodology aims to provide a robust comparison between Lagrangian and gridded Eulerian data sets.

> Coquereau, A. and Foukal, N. P.: A robust framework for comparing Lagrangian and gridded Eulerian velocity fields: an example application to surface drifters and altimetry-derived surface currents, EGUsphere [preprint], https://doi.org/10.5194/egusphere-2022-1450, 2022.


> Coquereau, A. and Foukal, N. P.: Evaluating altimetry-derived surface currents on the south Greenland shelf with surface drifters, Ocean Sci., 19, 1393–1411, https://doi.org/10.5194/os-19-1393-2023, 2023. 

## Requirements<a name="requirements"></a>

You can install all libraries used in the notebooks from the terminal with the following command:

```bash
conda create -n adsc_svp -c conda-forge parcels jupyter cartopy scikit-learn seaborn
```

To activate your virtual environment with the libraries installed, run:

```bash
conda activate adsc_svp
```

You can install motuclient from the terminal with the following command. It is required to download the different datasets directly from the terminal ([see details](https://help.marine.copernicus.eu/en/articles/4796533-what-are-the-motu-apis)). If you install the client with the environment activated, do not forget to activate it before using the client.

```bash
python -m pip install motuclient==1.8.4 --no-cache-dir
```

## Download data <a name="download"></a>

### Geostrophy data set <a name="geostrophy"></a>

The Geostrophy historical [data set](https://doi.org/10.48670/moi-00148) which is compared in the paper to Global Drifter Program (GDP) drifters can be downloaded with the following command. You must replace ```<USERNAME>``` and ```<PASSWORD>``` with your own credentials. If you do not have any, you can sign up [here](https://data.marine.copernicus.eu/register).

```bash
python -m motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id SEALEVEL_GLO_PHY_L4_MY_008_047-TDS --product-id cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.25deg_P1D --longitude-min -49 --longitude-max -40 --latitude-min 59 --latitude-max 62 --date-min "1993-01-02 00:00:00" --date-max "2021-12-31 23:59:59" --variable ugos --variable vgos --out-dir ./data/ADSC/ --out-name geo_daily_gdp.nc --user <USERNAME> --pwd <PASSWORD>
```

### Geostrophy+Ekman data set <a name="geostrophy_ekman"></a>

Similarly, the Geostrophy + Ekman historical [data set](https://doi.org/10.48670/moi-00050) which is compared to Global Drifter Program (GDP) drifters can be downloaded with the following command. The domain downloaded is a little bit larger to allow synthetic trajectories in the thrd step to exit the area of study before encountering limits of the available velocity field.

```bash
python -m motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id MULTIOBS_GLO_PHY_REP_015_004-TDS --product-id dataset-uv-rep-daily --longitude-min -50.5 --longitude-max -40 --latitude-min 58 --latitude-max 62 --date-min "1993-01-02 00:00:00" --date-max "2021-12-31 23:59:59" --depth-min 15 --depth-max 15 --variable uo --variable vo --out-dir ./data/ADSC/ --out-name geo_ekman_daily_gdp_new.nc --user <USERNAME> --pwd <PASSWORD>
````

### Global Drifter Program (GDP) trajectories data set <a name="gdp"></a>

GDP interpolated at 6-hourly frequency can be downloaded from the NOAA AOML Physical Oceanography Department [website](https://www.aoml.noaa.gov/phod/gdp/interpolated/data/subset.php).

Here we choose to download a subset of interpolated data with the following parameters. After entering those parameters, checked the "Drogue On Only Data" box and enter your email adress, you will receive the link to download your subset by email.

fromDate=1993/01/02\
toDate=2021/12/31\
\
northernEdge=62\
southernEdge=58\
westernEdge=-51\
easternEdge=-40\
\
Drogue=1 (checked)

### Bathymetry Data <a name="bathy"></a>

A set of bathymetric data is provided in the ```./data/bathy``` folder. It is a subset extracted from the General Bathymetric Chart of the Ocean (GEBCO) which can also be easily downloaded from the [GEBCO's website](https://download.gebco.net).
You can directly select the size of the domain you need. Here, the selected domain extent from 59° to 62°N and -49° to -40°E.

Credits: GEBCO Compilation Group (2022) GEBCO 2022 Grid (doi:10.5285/e0f0bb80- ab44-2739-e053-6c86abc0289c).

## 3-step methodology notebooks <a name="methodology"></a>

The methodology presented consists of three steps:
 - Point-wise comparison between gridded Eulerian and Lagrangian velocity fields (```./codes/point_wise_comparison.ipynb```)
 - Eulerian gridding of Lagrangian velocities (```./codes/eulerian_gridding.ipynb```)
 - Observed and synthetic trajectories (```./codes/synthetic_trajectories.ipynb```)
    
Each step is presented in a separate Python notebook in the ```./codes``` folder.
A Python notebook also makes it possible to process the data from the GDP drifter and to select only the values that interest us (```./codes/read_and_format_gdp_trajectories.ipynb```).
