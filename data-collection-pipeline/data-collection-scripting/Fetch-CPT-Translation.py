import logging

import requests
from bs4 import BeautifulSoup
import csv
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to fetch description
def fetch_description(url, container_id):
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.find(id=container_id)
    if container:
        description_p = container.find('p')
        if description_p:
            return description_p.get_text(strip=True)
        else:
            return "Description not found."
    else:
        return "Container not found."


# Headers for HTTP request
headers = {
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'host': 'www.aapc.com',
    # The cookie may need to be updated for your specific session or removed if not required.
    'Cookie': '.ASPXANONYMOUS=cfAZrYiqosuppjWWAsKnuGDzDVuI_f2Ool0Ykw6K4EJU7XwR3_XO0oWKbEmJe6AQ0kU6xzH2eWh7o5sV3PGRkMVfeexQF2HaPhPONn6xjZzRiWbzEbf-7c4vc35G43y7GB7i3g2; PHPSESSID=lb5pksik2dp4f1vppd1npeqa73'
}

# File paths
cpt_codes_file = "/CPT_CODES/cpt_codes.txt"
output_file = "../../data-cleaning-pipeline-generated-data/cpt-translation.csv"

# Read CPT codes from file
with open(cpt_codes_file, 'r') as file:
    cpt_codes = file.read().splitlines()

# Write to CSV
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["CPT Code", "Description"])

    for code in cpt_codes:
        cpt_url = f"https://www.aapc.com/codes/cpt-codes/{code}"
        description = fetch_description(cpt_url, "cpt_layterms")
        logging.info(f"Translation for code {code} found, saving it to CSV.")
        csvwriter.writerow([code, description])
