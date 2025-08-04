# Load the district boundary GeoJSON (ensure district names match your data)
districts_gdf = gpd.read_file("data/India Shapefile With Kashmir/India Shape/india_ds.shp")
districts_gdf["DISTRICT"] = districts_gdf["DISTRICT"].str.strip().str.lower()

districts_gdf.columns = districts_gdf.columns.str.strip().str.lower()
districts_gdf["district"] = districts_gdf["district"].str.strip().str.lower()
districts_gdf = districts_gdf[districts_gdf["state"].str.upper() == "MAHARASHTRA"].copy()

if 'district' not in districts_gdf.columns:
    # You may need to check the column name from your shapefile
    districts_gdf['district'] = districts_gdf['dist_name'].str.strip().str.lower()

# Path where the NDVI CSV files are stored
input_folder = "consolidated_by_year"
# output_folder = "ndvi_maps"
# os.makedirs(output_folder, exist_ok=True)

# Loop through each yearly CSV and generate a map
for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        year = file.split("_")[1].split(".")[0]
        df = pd.read_csv(os.path.join(input_folder, file))

        # Normalize district names
        df["district"] = df["district"].str.strip().str.lower()

        # Aggregate NDVI by district (already yearly, but doing mean again for safety)
        year_ndvi = df.groupby("district")["mean_ndvi"].mean().reset_index()

        # Merge with Maharashtra shapefile
        merged = districts_gdf.merge(year_ndvi, on="district", how="left")

        # Plot
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        merged.plot(column="mean_ndvi", cmap="RdYlGn", linewidth=0.8, ax=ax, edgecolor="0.8", legend=True)
        ax.set_title(f"Average NDVI - {year}", fontsize=14)
        ax.axis("off")

        # # Save the plot
        # plt.savefig(os.path.join(output_folder, f"ndvi_maharashtra_{year}.png"), bbox_inches="tight")
        # plt.close()
