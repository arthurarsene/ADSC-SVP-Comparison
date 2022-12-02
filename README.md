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

### Global Drifter Program (GDP) Comparison Experiment

##### Geostrophy+Ekman data set

The Geostrophy + Ekman historical [data set](https://doi.org/10.48670/moi-00050) compared to Global Drifter Program (GDP) drifters can be downloaded with the following command. You must replace ```<USERNAME>``` and ```<PASSWORD>``` with your own credentials. If you do not have any, you can register [here](https://data.marine.copernicus.eu/register).
(This can take a while)

```bash
python -m motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id MULTIOBS_GLO_PHY_REP_015_004-TDS --product-id dataset-uv-rep-hourly --longitude-min -49 --longitude-max -41 --latitude-min 59 --latitude-max 62 --date-min "1993-01-01 00:00:00" --date-max "2021-12-31 21:00:00" --depth-min 15 --depth-max 15 --variable uo --variable vo --out-dir ./data/ --out-name geo_ekman_gdp --user <USERNAME> --pwd <PASSWORD>
```

##### GDP trajectories data set

To do

### Experiment wih drifters from GFWE and TERIFIC

##### Drifters trajectories

To do

##### Altimetry-derived surface currents

To do

##### Bathymetry Data

GEBCO

https://download.gebco.net
