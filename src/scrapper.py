import os
import requests

base_url = "https://bhuvan-app3.nrsc.gov.in/isroeodatadownloadutility/tiledownloadnew_cfr_new.php?f=ocm2_ndvi_filt_"
times = ["01to15", "16to30", "16to31", "16to28"]
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
years = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]

def is_leap_year(year):
    year = int(year)
    if (year%4 == 0):
        if (year % 100 != 0) or (year % 400 == 0):
            return True
    return False

folder = "data/downloads"
os.makedirs(folder, exist_ok=True)

def scrapper_req(time_list, month, years_list=None):
    if years_list is None:
        years_list = years
    for year in years_list:
        current_times = time_list.copy()
        if is_leap_year(year) and month == "feb":
            current_times = ["01to15", "16to29"]  # Only February changes for leap years
        for time in current_times:
            url = f"{base_url}{time}_{month}{year}_v01_01.zip&se=OCM2&u=Arush01"
            response = requests.get(url, stream=True)
            filename = f"{time}+{month}_{year}.zip"
            filepath = os.path.join(folder, filename)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"Download completed: {filepath}")
            else:
                print(f"Failed to download. Status code: {response.status_code}")

if __name__ == "__main__":
    for month in months:
        if month in ["jan", "mar", "may", "jul", "aug", "oct", "dec"]:
            scrapper_req(["01to15", "16to31"], month)
        elif month in ["apr", "jun", "sep", "nov"]:
            scrapper_req(["01to15", "16to30"], month)
        else:  # Only "feb"
            scrapper_req(["01to15", "16to28"], month)



        
    
