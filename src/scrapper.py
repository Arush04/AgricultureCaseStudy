import requests
import zipfile

base_url = "https://bhuvan-app3.nrsc.gov.in/isroeodatadownloadutility/tiledownloadnew_cfr_new.php?f=ocm2_ndvi_filt_"
times = ["01to15", "16to30", "16to31", "16to28"]
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
years = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

def scrapper_req(time_list):
    for year in years:
        for time in time_list:
            url = f"{base_url}{time}_{month}{year}_v01_01.zip&se=OCM2&u=Arush01"
            response = requests.get(url, stream=True)
            filename = f"{time}+{month}_{year}.zip"
            # Check if request was successful
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"Download completed: {filename}")
            else:
                print(f"Failed to download. Status code: {response.status_code}")

for month in months:
    if month in ["jan", "mar", "may", "jul", "aug", "oct", "dec"]:
        times_new = []
        times_new.append(times[0])
        times_new.append(times[2])
        scrapper_req(times_new)
        
    elif month in ["apr", "jun", "sep", "nov"]:
        times_new = []
        times_new.append(times[0])
        times_new.append(times[1])
        scrapper_req(times_new)
    else:
        times_new = []
        times_new.append(times[0])
        times_new.append(times[3])
        scrapper_req(times_new)

        
    
