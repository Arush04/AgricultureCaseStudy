<p align="center"><h1 align="center">AGRICULTURE CASE STUDY</h1></p>
<p align="center">
	<img src="https://img.shields.io/github/last-commit/Arush04/AgricultureCaseStudy?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Arush04/AgricultureCaseStudy?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Arush04/AgricultureCaseStudy?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>

##  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Project Structure](#-project-structure)
  - [ Project Index](#-project-index)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#-prerequisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Testing](#-testing)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview
This project, undertaken for agricultural policymakers and stakeholders in the Indian states of Maharashtra (MH) and Madhya Pradesh (MP), aimed to comprehensively assess and strengthen climate resiliency in regional agriculture—a critical issue for these states’ millions of farming families, given the mounting risks from unpredictable rainfall, temperature shifts, and frequent extreme weather. The initiative’s scope spanned deep-dive climate data analysis (including ten years’ temperature, rainfall, and NDVI satellite data), district-level crop performance evaluations, economic impact assessments, infrastructure and technology review, and policy effectiveness audits.  

---
##  Project Structure

```sh
└── AgricultureCaseStudy/
    ├── README.md
    ├── data
    │   └── raw
    ├── requirements.txt
    └── src
        ├── config.py
        ├── extractor.py
        ├── main_MH.py
        ├── main_MP.py
        ├── plot_graphs.py
        ├── scrapper.py
        ├── visualize_mh.py
        └── visualize_mp.py
```

---
##  Getting Started

###  Prerequisites

Before getting started with AgricultureCaseStudy, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip


###  Installation

Install AgricultureCaseStudy using one of the following methods:

**Build from source:**

1. Clone the AgricultureCaseStudy repository:
```sh
❯ git clone https://github.com/Arush04/AgricultureCaseStudy
```

2. Navigate to the project directory:
```sh
❯ cd AgricultureCaseStudy
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```




###  Steps
Make sure the requirements are installed and environment activated  
1. Make use of the scrapper to download raster files:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python src/scrapper.py
```
This will download files in `data/download` folder  

2. Check out to the downloads folder and select and extract all zip files, once extracted move all files to a new folder called `ndvi_files` in the data folder
3. Then run this from root
```sh
❯ python src/extractor.py
```
This extracts all .tif files from the `ndvi_files` folder and saves them in the `data/tif_files`  

4. Now we have all data, now run 
```sh
❯ python src/main_MH.py # for MP run src/main_MP.py
```
This creates a folder called `analysis_MH` in the root directory which contains year-wise csv files with data like mean_temp, mean_ndvi, rainfall(in mm) for each district of Mahrashtra  

5. For plotting graphs we have 3 options:
   ```
	1 is for NDVI vs mean temp and rainfall
   	2 is for NDVI concentration for different temp and rainfall ranges
   	3 is NDVI vs temp and NDVI vs rainfall trend line
   ```
To get these graphs run the following:
```sh
❯ python src/plot_graphs.py --plot_function <option> --input_folder <folder with csv files we get from running main_MH>
```

6.  Similarly to visualize district wise average NDVI per year run the following:
```sh
❯ python src/visualize_mh.py --input_folder <older with csv files we get from running main_MH> --output_folder <your output folder>
```

###  Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pytest
```
