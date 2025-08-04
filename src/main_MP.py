import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
import rasterstats
from rasterstats import zonal_stats
import os
from datetime import datetime
from tqdm import tqdm
import argparse
from config import Configuration

# === Add Crop Mapping ===
crop_map = {
    "MP": {
        "Kharif": ["PA", "SB"],
        "Rabi": ["WH", "GM"]
    }
}

def assign_crops(state, season):
    return crop_map.get(state, {}).get(season, [])

# === Define Seasonal Mapping for Maharashtra ===
def get_season(month):
    if month in [6, 7, 8, 9, 10]:
        return "Kharif"
    elif month in [11, 12, 1, 2, 3, 4]:
        return "Rabi"
    else:
        return "Other"

def mp_data_ingestion(shp_file, rain_df, temp_df, ndvi, output):
    # === Load District Shapefile and Filter for Madhya Pradesh ===
    mp_gdf = gpd.read_file(shp_file)
    
    # === Load Climate Data (Provided from case study) ===
    rain_df = pd.read_csv(rain_df, parse_dates=["date"])
    temp_df = pd.read_csv(temp_df, parse_dates=["date"])
    
    # === The following are the names mismatch between the csv files and the GIS shapefile ===
    district_rename_map = {
        "NARSINGPUR": "NARSIMHAPUR"
    }
    
    # === Replace the names in csv files with names from GIS shape file ===
    rain_df["District"] = rain_df["District"].replace(district_rename_map)
    temp_df["District"] = temp_df["District"].replace(district_rename_map)
    
    # === Creating new columns to support findings ===
    for df in [rain_df, temp_df]:
        df["month"] = df["date"].dt.month
        df["season"] = df["month"].apply(get_season)
        df["year"] = df["date"].dt.year
    
    # === Process NDVI Files ===
    ndvi_folder = ndvi
    ndvi_stats_list = []
    
    # === Looping through NDVI files and extracting data ===
    for file in tqdm(os.listdir(ndvi_folder), desc="Processing NDVI files"):
        if file.endswith(".tif"):
            try:
                parts = file.split("_")
                month = parts[1].lower()[:3]
                year = int(parts[2])
                month_num = datetime.strptime(month, "%b").month
                season = get_season(month_num)
            except:
                continue
    
            ndvi_path = os.path.join(ndvi_folder, file)
            with rasterio.open(ndvi_path) as src:
                ndvi_data = src.read(1).astype("float32")
                ndvi_data[ndvi_data == src.nodata] = np.nan
                ndvi_data = (ndvi_data / 255.0)
                
                stats = zonal_stats(
                    mp_gdf, ndvi_data, affine=src.transform,
                    stats=["mean"], geojson_out=True
                )
    
                for feature, stat in zip(mp_gdf.iterrows(), stats):
                    district_name = feature[1]["dtname"]
                    ndvi_stats_list.append({
                        "district": district_name,
                        "season": season,
                        "month": month_num,
                        "year": year,
                        "mean_ndvi": stat["properties"]["mean"]
                    })
    
    ndvi_df = pd.DataFrame(ndvi_stats_list)
    
    # === Standardize district names across all DataFrames (they are capital in GIS file and small in csv files) ===
    ndvi_df["district"] = ndvi_df["district"].str.strip().str.lower()
    temp_df["district"] = temp_df["District"].str.strip().str.lower()
    rain_df["district"] = rain_df["District"].str.strip().str.lower()
    
    # === Calculate monthly mean NDVI for each district and get mean temp and rainfall_mm values===
    ndvi_monthly = ndvi_df.groupby(["district", "season", "month", "year"]).agg(mean_ndvi=("mean_ndvi", "mean")).reset_index()
    temp_monthly = temp_df.groupby(["district", "season", "month", "year", "min", "max"]).agg(mean_temp=("mean", "mean")).reset_index()
    rainfall_monthly = rain_df.groupby(["district", "season", "month", "year"]).agg(rainfall_mm=("rainfall_mm", "mean")).reset_index()
    
    # === Merge the dataframes on common keys ===
    merged = pd.merge(ndvi_monthly, temp_monthly, on=["district", "season", "month", "year"], how="left")
    merged = pd.merge(merged, rainfall_monthly, on=["district", "season", "month", "year"], how="left")
    merged = merged.rename(columns={"min": "min_temp", "max": "max_temp", "rainfall_mm": "mean_rainfall(mm)"})
    
    merged["state"] = "Madhya Pradesh"
    merged["crops"] = merged.apply(lambda row: assign_crops(row["state"], row["season"]), axis=1)
        
    # === Save separate CSVs for each year ===
    output_folder = "analysis_MP"
    os.makedirs(output_folder, exist_ok=True)
    
    for year in merged["year"].unique():
        yearly_df = merged[merged["year"] == year]
        yearly_df.to_csv(f"{output_folder}/climate_{year}.csv", index=False)


if __name__=="__main__":
    cfg = Configuration()

    parser = argparse.ArgumentParser(description='Data ingestion pipeline')
    parser.add_argument('--shape_file', type=str, default=cfg.district_shp_file_mp, help='Path to district Shape file for the state')
    parser.add_argument('--rain_df', type=str, default=cfg.rain_df_mp, help='Path to rain csv file of state')
    parser.add_argument('--temp_df', type=str, default=cfg.temp_df_mp, help='Path to temperature csv file of state')
    parser.add_argument('--ndvi', type=str, default=cfg.ndvi_folder, help='Path to folder with NDVI files')
    parser.add_argument('--output', type=str, default=cfg.output_folder_mh, help='Path of output folder to save csv files')
    args = parser.parse_args()
    
    mp_data_ingestion(shp_file=args.shape_file, rain_df=args.rain_df, temp_df=args.temp_df, ndvi=args.ndvi, output=args.output)
    
# # === Save or visualize ===
# climate_crop_df.to_csv("climate_crop_analysis_maharashtra.csv", index=False)
# print(climate_crop_df.head())
