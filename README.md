### Data access

##### The Geostrophy + Ekman is accessible with the following command:

python -m motuclient --motu https://my.cmems-du.eu/motu-web/Motu --service-id MULTIOBS_GLO_PHY_REP_015_004-TDS --product-id dataset-uv-rep-hourly --longitude-min -49 --longitude-max -41 --latitude-min 59 --latitude-max 62 --date-min "1993-01-01 00:00:00" --date-max "2021-12-31 21:00:00" --depth-min 15 --depth-max 15 --variable uo --variable vo --out-dir <OUTPUT_DIRECTORY> --out-name <OUTPUT_FILENAME> --user <USERNAME> --pwd <PASSWORD>