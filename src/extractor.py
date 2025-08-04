import os
import shutil
import glob
from pathlib import Path

def extract_tif_files(source_dir=".", target_dir="extracted_tifs"):
    """
    Extract TIF files from all subdirectories and rename them
    
    Args:
        source_dir: Directory containing the folders with TIF files
        target_dir: Directory where extracted TIF files will be saved
    """
    
    # Create target directory if it doesn't exist
    Path(target_dir).mkdir(exist_ok=True)
    
    # Get all directories in the source directory
    all_items = os.listdir(source_dir)
    directories = [item for item in all_items if os.path.isdir(os.path.join(source_dir, item))]
    
    print(f"Found {len(directories)} directories to process:")
    for d in directories:
        print(f"  {d}")
    
    if not directories:
        print("No directories found!")
        return
    
    extracted_count = 0
    
    for dir_name in directories:
        dir_path = os.path.join(source_dir, dir_name)
        print(f"\nProcessing directory: {dir_name}")
        
        # Find TIF files in the directory (including subdirectories)
        tif_extensions = ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]
        all_tif_files = []
        
        for ext in tif_extensions:
            tif_pattern = os.path.join(dir_path, "**", ext)
            tif_files = glob.glob(tif_pattern, recursive=True)
            all_tif_files.extend(tif_files)
        
        print(f"  Found {len(all_tif_files)} TIF files")
        
        if all_tif_files:
            for tif_file in all_tif_files:
                # Extract parts from directory name
                # Handle both + and _ separators
                dir_name_clean = dir_name.replace('+', '_')
                parts = dir_name_clean.split('_')
                
                print(f"    Processing: {os.path.basename(tif_file)}")
                
                if len(parts) >= 2:
                    time_range = parts[0]  # 01to15
                    
                    # Try to extract month and year
                    if len(parts) >= 3:
                        month = parts[1]       # apr
                        year = parts[2]        # 2019
                    else:
                        # If only 2 parts, second part might be month+year
                        month_year = parts[1]
                        # Try to extract year (last 4 digits)
                        if len(month_year) > 4 and month_year[-4:].isdigit():
                            year = month_year[-4:]
                            month = month_year[:-4]
                        else:
                            month = month_year
                            year = "unknown"
                    
                    # Create new filename
                    original_name = os.path.basename(tif_file)
                    extension = os.path.splitext(original_name)[1]
                    
                    # New naming format: NDVI_month_year_timerange.tif
                    new_filename = f"NDVI_{month}_{year}_{time_range}{extension}"
                    
                    # Full path for new file
                    new_file_path = os.path.join(target_dir, new_filename)
                    
                    # Handle duplicate filenames
                    counter = 1
                    base_new_file_path = new_file_path
                    while os.path.exists(new_file_path):
                        name_part = os.path.splitext(base_new_file_path)[0]
                        ext_part = os.path.splitext(base_new_file_path)[1]
                        new_file_path = f"{name_part}_{counter}{ext_part}"
                        counter += 1
                    
                    # Copy the file
                    try:
                        shutil.copy2(tif_file, new_file_path)
                        print(f"      -> {os.path.basename(new_file_path)}")
                        extracted_count += 1
                    except Exception as e:
                        print(f"      Error: {e}")
                else:
                    # If we can't parse the directory name, just use it as is
                    original_name = os.path.basename(tif_file)
                    extension = os.path.splitext(original_name)[1]
                    new_filename = f"{dir_name}_{original_name}"
                    new_file_path = os.path.join(target_dir, new_filename)
                    
                    try:
                        shutil.copy2(tif_file, new_file_path)
                        print(f"      -> {new_filename}")
                        extracted_count += 1
                    except Exception as e:
                        print(f"      Error: {e}")
        else:
            print(f"    No TIF files found")
    
    print(f"\nExtraction complete! Total files extracted: {extracted_count}")
    print(f"Files saved to: {os.path.abspath(target_dir)}")

if __name__ == "__main__":
    extract_tif_files(source_dir="ndvi_data", target_dir="tif_files_new")