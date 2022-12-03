### Requirements

You can install all libraries used in the notebooks from the terminal with the following command:

```bash
conda create -n adsc_svp -c conda-forge parcels jupyter cartopy scikit-learn seaborn
```

To activate your virtual environment with the installed librairies, run:

```bash
conda activate adsc_svp
```

You can install motuclient from the terminal with the following command. It is required to download the different datasets directly from the terminal ([see details](https://help.marine.copernicus.eu/en/articles/4796533-what-are-the-motu-apis)). You can install the client with the environment activated; in this case do not forget to activate it to use the client.

```bash
python -m pip install motuclient==1.8.4 --no-cache-dir
```

## Download the data

### Geostrophy+Ekman data set

The Geostrophy + Ekman historical [data set](https://doi.org/10.48670/moi-00050) compared to Global Drifter Program (GDP) drifters can be downloaded with the following command. You must replace ```<USERNAME>``` and ```<PASSWORD>``` with your own credentials. If you do not have any, you can register [here](https://data.marine.copernicus.eu/register).
(This can take a while)

```bash
python -m motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id MULTIOBS_GLO_PHY_REP_015_004-TDS --product-id dataset-uv-rep-daily --longitude-min -49 --longitude-max -40 --latitude-min 59 --latitude-max 62 --date-min "1993-01-02 00:00:00" --date-max "2021-12-31 23:59:59" --depth-min 15 --depth-max 15 --variable uo --variable vo --out-dir ./data/ADSC/ --out-name geo_ekman_daily_gdp.nc --user <USERNAME> --pwd <PASSWORD>
```

### GDP trajectories data set

Your submitted request was: request_gld.20221202_104507
Drogue=1
fromDate=1993/01/02
toDate=2021/12/31
northernEdge=62
southernEdge=59
westernEdge=-49
easternEdge=-40


### Bathymetry Data

A bathymetry data set is provided in the ```./data/bathy``` folder. It is a subset extracted from the General bathymetric Chart of the Ocean (GEBCO) that can be also easily downloaded from the [GEBCO's website](https://download.gebco.net).
You can directly select the size of the domain you need. Here, the selected domain extent from 59° to 62°N and -49° to -40°E.

Credits: GEBCO Compilation Group (2022) GEBCO 2022 Grid (doi:10.5285/e0f0bb80- ab44-2739-e053-6c86abc0289c).