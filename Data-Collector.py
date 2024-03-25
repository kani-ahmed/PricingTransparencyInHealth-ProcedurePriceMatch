import json
import os
import re
from urllib.parse import unquote, urlparse

import requests
from tqdm import tqdm

# Suppress warnings from unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Define states and their respective ZIP codes
states_with_zip_codes = {
    "OH": [""],
}

# Base directory for downloaded files
base_dir = 'Hospital Price Transparency Data'
if not os.path.exists(base_dir):
    os.makedirs(base_dir, exist_ok=True)

# Initialize session with headers
session = requests.Session()
session.headers.update({
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'sessionid': '5087494111016062868872034',
})
session.verify = False  # Apply verify=False to the entire session to bypass SSL certificate verification

# Headers specifically for downloading files
download_headers = {
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'host': 'storage.patientrightsadvocatefiles.org'
}
# Initialize the progress bar with an initial total of 0
progress_bar = tqdm(total=0, desc="Preparing to download files", unit="file")

# File to track downloaded and failed downloads
progress_file = 'download_progress.json'
if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        progress = json.load(f)
else:
    progress = {"downloaded": [], "failed": []}


def log_progress():
    with open(progress_file, 'w') as f:
        json.dump(progress, f, indent=4)


for state, zip_codes in states_with_zip_codes.items():
    for zip_code in zip_codes:
        # Construct the search URL
        search_url = f"https://pts.patientrightsadvocatefiles.org/facility/search?searchstate={state}"
        if zip_code:
            search_url += f"&search={zip_code}"

        response = session.get(search_url)  # Use session to make the request
        if response.status_code != 200:
            print(f"Error fetching data for {state} {zip_code}: {response.status_code}")
            continue

        facilities = response.json()

        # Update the total number of files to download
        batch_total_files = sum(len(facility["files"]) for facility in facilities)
        progress_bar.total += batch_total_files
        progress_bar.refresh()  # Refresh to display the updated total

        for facility in facilities:
            city = facility["city"]
            zip_code = facility["zip"] if zip_code else "Unknown ZIP"
            facility_name = re.sub(r'[\\/*?:"<>|]', "", facility["name"]).replace(' ', '_')
            # directory_path = os.path.join(base_dir, state, zip_code if zip_code else "Statewide", facility_name)

            # Adjusting directory path to include city and ZIP code for better organization
            directory_path = os.path.join(base_dir, state, city, zip_code, facility_name)
            os.makedirs(directory_path, exist_ok=True)

            for file in facility["files"]:
                download_url = f"https://storage.patientrightsadvocatefiles.org/{file['project']}/{file['storage']}"
                safe_filename = re.sub(r'[\\/*?:"<>|]', "",
                                       unquote(urlparse(download_url).path.split('/')[-1])).replace(' ', '_')
                save_path = os.path.join(directory_path, safe_filename)

                if save_path in progress["downloaded"]:
                    print(f"Already downloaded: {save_path}")
                    continue
                try:
                    with session.get(download_url, headers=download_headers,
                                     stream=True) as r:  # Use session to make the request
                        r.raise_for_status()  # Ensure the request was successful
                        with open(save_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=1024):
                                f.write(chunk)
                                progress["downloaded"].append(save_path)
                    progress_bar.update(1)  # Increment the progress bar for each file downloaded
                    print(f"Downloaded {save_path}")
                except Exception as e:
                    print(f"Failed to download {save_path}: {e}")
                    progress["failed"].append({"path": save_path, "url": download_url, "error": str(e)})
                finally:
                    log_progress()

# Close the progress bar after all downloads are completed
progress_bar.close()
print("Download process completed.")
