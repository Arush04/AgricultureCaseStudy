import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from config import Configuration

def draw_ndvi_map(shape_file, input_folder, output_folder):
    districts_gdf = gpd.read_file(shape_file)
    districts_gdf["dtname"] = districts_gdf["dtname"].str.strip().str.lower()

    districts_gdf.columns = districts_gdf.columns.str.strip().str.lower()
    districts_gdf["district"] = districts_gdf["dtname"].str.strip().str.lower()
    districts_gdf = districts_gdf[districts_gdf["stname"].str.upper() == "MADHYA PRADESH"].copy()

    global_min = 0.0
    global_max = 255

    # Check if output folder exists, create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    else:
        print(f"Folder already exists: {output_folder}")

    # Now create plots with uniform legend
    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            year = file.split("_")[1].split(".")[0]
            df = pd.read_csv(os.path.join(input_folder, file))
            df["district"] = df["district"].str.strip().str.lower()

            # Aggregate NDVI by district
            year_ndvi = df.groupby("district")["mean_ndvi"].mean().reset_index()
            year_ndvi["mean_ndvi"] = year_ndvi["mean_ndvi"] * 255

            # Merge with Maharashtra shapefile
            merged = districts_gdf.merge(year_ndvi, on="district", how="left")

            # Plot with fixed vmin/vmax
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            merged.plot(
                column="mean_ndvi",
                cmap="RdYlGn",
                linewidth=0.8,
                ax=ax,
                edgecolor="0.8",
                legend=True,
                vmin=global_min,
                vmax=global_max
            )

            ax.set_title(f"Average NDVI - {year}", fontsize=14)
            ax.axis("off")

            plt.tight_layout()
            plt.savefig(f"{output_folder}/ndvi_map_{year}.png", dpi=300, bbox_inches="tight")
            plt.show()

if __name__=="__main__":
    cfg = Configuration()

    parser = argparse.ArgumentParser(description='Draw NDVI State Map')
    parser.add_argument('--shape_file', type=str, default=cfg.district_shp_file_mp, help='Path to district Shape file for the state')
    parser.add_argument('--input_folder', type=str, required=True, help='Path to folder with CSV files with per year data of State')
    parser.add_argument('--output_folder', type=str, required=True, help='Path of output folder to save csv files')
    args = parser.parse_args()

    draw_ndvi_map(shape_file=args.shape_file, input_folder=args.input_folder, output_folder=args.output_folder)
