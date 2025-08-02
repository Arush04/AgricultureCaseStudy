import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
import rasterstats
from rasterstats import zonal_stats
import os
from datetime import datetime
from tqdm import tqdm

# === Load District Shapefile and Filter for Maharashtra ===
districts_gdf = gpd.read_file("data/India Shapefile With Kashmir/India Shape/india_ds.shp")
maha_gdf = districts_gdf[districts_gdf["STATE"].str.upper() == "MAHARASHTRA"].copy()

# === Define Seasonal Mapping for Maharashtra ===
def get_season(month):
    if month in [6, 7, 8, 9, 10]:
        return "Kharif"
    elif month in [11, 12, 1, 2, 3, 4]:
        return "Rabi"
    else:
        return "Other"

# === Load Climate Data (Provided from case study) ===
rain_df = pd.read_csv("data/MH_precipitation.csv", parse_dates=["date"])
temp_df = pd.read_csv("data/MH_temperature.csv", parse_dates=["date"])

# === The following are the names mismatch between the csv files and the GIS shapefile, Could only find this shapefile which is old hence needs some pre-processing ===
district_rename_map = {
    "BEED": "BID",
    "BULDHANA": "BULDANA",
    "NASIK": "NASHIK",
    "AHMEDNAGAR": "AHMADNAGAR",
    "RAIGAD": "RAIGARH",
    "GARHCHIROLI": "GADCHIROLI"
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
ndvi_folder = "data/tif_files"
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
                maha_gdf, ndvi_data, affine=src.transform,
                stats=["mean"], geojson_out=True
            )

            for feature, stat in zip(maha_gdf.iterrows(), stats):
                district_name = feature[1]["DISTRICT"]
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
temp_df["District"] = temp_df["District"].str.strip().str.lower()
rain_df["District"] = rain_df["District"].str.strip().str.lower()

# === Rename columns for consistency ===
temp_df = temp_df.rename(columns={"District": "district", "Mean_Temperature": "mean_temp"})
rain_df = rain_df.rename(columns={"District": "district", "Rainfall_mm": "rainfall_mm"})

# === Calculate monthly mean for each district ===
ndvi_monthly = ndvi_df.groupby(["district", "season", "month", "year"]).agg(mean_ndvi=("mean_ndvi", "mean")).reset_index()
temp_monthly = temp_df.groupby(["district", "season", "month", "year"]).agg(mean_temp=("mean", "mean")).reset_index()
rainfall_monthly = rain_df.groupby(["district", "season", "month", "year"]).agg(rainfall_mm=("rainfall_mm", "mean")).reset_index()

# === Merge the dataframes on common keys ===
merged = pd.merge(ndvi_monthly, temp_monthly, on=["district", "season", "month", "year"], how="left")
merged = pd.merge(merged, rainfall_monthly, on=["district", "season", "month", "year"], how="left")

# === Add Crop Mapping ===
crop_map = {
    "Maharashtra": {
        "Kharif": ["CO", "SB"],
        "Rabi": ["WH", "GM"]
    }
}

def assign_crops(state, season):
    return crop_map.get(state, {}).get(season, [])

merged["state"] = "Maharashtra"
merged["crops"] = merged.apply(lambda row: assign_crops(row["state"], row["season"]), axis=1)
    
# === Save separate CSVs for each year ===
output_folder = "analysis"
os.makedirs(output_folder, exist_ok=True)

for year in merged["year"].unique():
    yearly_df = merged[merged["year"] == year]
    yearly_df.to_csv(f"{output_folder}/climate_{year}.csv", index=False)


# # === Save or visualize ===
# climate_crop_df.to_csv("climate_crop_analysis_maharashtra.csv", index=False)
# print(climate_crop_df.head())