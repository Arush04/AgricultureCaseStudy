import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


def ndvi_vs_temp_n_rainfall(folder_path):
    file_prefix = "climate_"

    # -----------------------------
    # STEP 1: Load all CSV files
    # -----------------------------
    all_dfs = []

    for file in os.listdir(folder_path):
        if file.startswith(file_prefix) and file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            all_dfs.append(df)

    climate_df = pd.concat(all_dfs, ignore_index=True)

    # Drop rows with missing values
    climate_df = climate_df.dropna(subset=['mean_ndvi', 'mean_temp', 'mean_rainfall(mm)', 'year'])

    # -----------------------------
    # STEP 2: Plotting all graphs
    # -----------------------------
    sns.set(style="whitegrid")
    fig, axs = plt.subplots(1, 3, figsize=(20, 6))

    # === Plot 1: NDVI vs Mean Temperature
    sns.scatterplot(data=climate_df, x='mean_temp', y='mean_ndvi', hue='season', alpha=0.6, ax=axs[0])
    axs[0].set_title('NDVI vs Mean Temperature')
    axs[0].set_xlabel('Mean Temperature (°C)')
    axs[0].set_ylabel('Mean NDVI')

    # === Plot 2: NDVI vs Mean Rainfall
    sns.scatterplot(data=climate_df, x='mean_rainfall(mm)', y='mean_ndvi', hue='season', alpha=0.6, ax=axs[1])
    axs[1].set_title('NDVI vs Mean Rainfall')
    axs[1].set_xlabel('Mean Rainfall (mm)')
    axs[1].set_ylabel('Mean NDVI')

    # === Plot 3: NDVI vs Year (mean across all districts)
    yearly_ndvi = climate_df.groupby('year')['mean_ndvi'].mean().reset_index()
    sns.lineplot(data=yearly_ndvi, x='year', y='mean_ndvi', marker='o', ax=axs[2])
    axs[2].set_title('NDVI Trend Over Years')
    axs[2].set_xlabel('Year')
    axs[2].set_ylabel('Average NDVI')
    plt.tight_layout()
    plt.show()

def ndvi_conc_temp_n_rainfall(folder_path):
    file_prefix = "climate_"
    all_dfs = []

    for file in os.listdir(folder_path):
        if file.startswith(file_prefix) and file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder_path, file))
            all_dfs.append(df)

    climate_df = pd.concat(all_dfs, ignore_index=True)

    # Drop rows with missing critical values
    climate_df = climate_df.dropna(subset=['mean_ndvi', 'mean_temp', 'mean_rainfall(mm)'])
    temp_bins = np.arange(int(climate_df['mean_temp'].min()), int(climate_df['mean_temp'].max()) + 1, 1)
    rain_bins = np.arange(0, int(climate_df['mean_rainfall(mm)'].max()) + 10, 10)  # 10mm intervals

    climate_df['temp_bin'] = pd.cut(climate_df['mean_temp'], bins=temp_bins)
    climate_df['rain_bin'] = pd.cut(climate_df['mean_rainfall(mm)'], bins=rain_bins)
    binned_ndvi = climate_df.groupby(['temp_bin', 'rain_bin'])['mean_ndvi'].mean().reset_index()

    # Drop NaNs
    binned_ndvi = binned_ndvi.dropna(subset=['mean_ndvi'])
    top_ndvi = binned_ndvi.sort_values(by='mean_ndvi', ascending=False).head(5)

    print("\nTop 5 temperature and rainfall ranges with highest average NDVI:\n")
    for _, row in top_ndvi.iterrows():
        print(f"Temperature: {row['temp_bin']}, Rainfall: {row['rain_bin']}, Mean NDVI: {row['mean_ndvi']:.3f}")
    pivot_table = binned_ndvi.pivot(index='temp_bin', columns='rain_bin', values='mean_ndvi')

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap='RdYlGn', annot=True, fmt=".2f", cbar_kws={'label': 'Mean NDVI'})
    plt.title('NDVI Concentration by Temperature and Rainfall Ranges')
    plt.xlabel('Rainfall Range (mm)')
    plt.ylabel('Temperature Range (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def temp_n_rainfall(folder_path):
    file_prefix = "climate_"
    all_dfs = []

    for file in os.listdir(folder_path):
        if file.startswith(file_prefix) and file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder_path, file))
            all_dfs.append(df)

    df = pd.concat(all_dfs, ignore_index=True)
    yearly_data = df.groupby('year').agg({
        'mean_temp': 'mean',
        'mean_rainfall(mm)': 'mean'
    }).reset_index()

    # Create two subplots side by side
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Year vs Mean Temperature
    axs[0].plot(yearly_data['year'], yearly_data['mean_temp'], color='red', marker='o')
    axs[0].set_title('Year-wise Mean Temperature')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Temperature (°C)')
    axs[0].grid(True)

    # Plot 2: Year vs Mean Rainfall
    axs[1].plot(yearly_data['year'], yearly_data['mean_rainfall(mm)'], color='blue', marker='s')
    axs[1].set_title('Year-wise Mean Rainfall')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Rainfall (mm)')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    cfg = Configuration()
    print("choose 1 for ")
    print("choose 2 for ")
    print("choose 3 for ")
    parser = argparse.ArgumentParser(description='Draw NDVI State Map')
    parser.add_argument('--plot_function', required=True, type=str, help='Which Plot you want?')
    parser.add_argument('--input_folder', type=str, required=True,help='Path to folder with CSV files with per year data of State')
    args = parser.parse_args()

    if args.plot_function == "1":
        ndvi_vs_temp_n_rainfall(folder_path=args.input_folder)
    elif args.plot_function == "2":
        ndvi_conc_temp_n_rainfall(folder_path=args.input_folder)
    elif args.plot_function == "3":
        temp_n_rainfall(folder_path=args.input_folder)
    else:
        print("enter valid choice")
