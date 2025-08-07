from dataclasses import dataclass

@dataclass
class Configuration:
    district_shp_file_mh = "data/MAHARASHTRA_DISTRICTS.geojson"
    district_shp_file_mp = "data/MADHYA PRADESH_DISTRICTS.geojson"
    rain_df_mh = "data/raw/MH_precipitation.csv"
    temp_df_mh = "data/raw/MH_temperature.csv"
    rain_df_mp = "data/raw/MP_precipitation.csv"
    temp_df_mp = "data/raw/MP_temperature.csv"
    ndvi_folder = "data/tif_files"
    output_folder_mh = "analysis_MH"
    outut_folder_mp = "analysis_MP"
