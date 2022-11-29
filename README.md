### Requirements

You can install all librairies used in the notebooks from the terminal with the following command:

```bash
conda create -n adsc_svp -c conda-forge parcels jupyter cartopy scikit-learn seaborn
```

You can install motuclient from the terminal with the following command. It is required to download the different datasets directly from the terminal.

```bash
python -m pip install motuclient==1.8.4 --no-cache-dir
```

### Data access

The Geostrophy + Ekman historical data set compared to Global Drifter Program (GDP) drifters can be downloaded with the following command. (It can take few minutes before the download starts)

```bash
python -m motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id MULTIOBS_GLO_PHY_REP_015_004-TDS --product-id dataset-uv-rep-hourly --longitude-min -49 --longitude-max -41 --latitude-min 59 --latitude-max 62 --date-min "1993-01-01 00:00:00" --date-max "2021-12-31 21:00:00" --depth-min 15 --depth-max 15 --variable uo --variable vo --out-dir ./data/ --out-name geo_ekman_gdp --user <USERNAME> --pwd <PASSWORD>
```