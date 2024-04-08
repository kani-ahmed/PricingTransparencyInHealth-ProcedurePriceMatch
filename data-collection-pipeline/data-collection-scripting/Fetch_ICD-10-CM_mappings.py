import requests

import urllib3
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import csv
import os
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Suppress SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

url = "https://www.aapc.com/codes/cpt_icd/ajax_cpt_crossref_icd10_char_short"

headers = {
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Accept': 'text/plain, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'host': 'www.aapc.com',
    'Cookie': '.ASPXANONYMOUS=katEZc2YTE-5pPmMnUtSSqJH-I4kDlJIrRv7OwSRGthJXxAcONC89fZI5tEwQ0IjOoASRZphGe5-5RwqyBSHzHz54mjqEqJT8snrGUttT-Lr1Xm9Gypq3VmemQ-emjSFlbvRwQ2; .ASPXAUTH=36310F697B786F1FD51CF0172C13FD9AC12D414A2B72CC6FF0848D8CB1924ECAD2C4448C58DBD38EE90C2A19C411A277F600535B891F8A21BC843FE4B018ABD12A41E93E923E5375BF90E53B1C9C418647AC3146A0820AD0C163E3DEAE014D5D861C8C13; .AspNet.Cookies=FgJNzXFKEhHGfoiIni29MoEnVSAlVWtHrg8bLcYH1F1QX-BS4uGBnGHAnOUXAHttyACEpBaxIcmQZeROfJ2H-EPtITp7-FfH89WvK5Nnf-J3VNaw_zOzuWDyVE9TJk22OcMxn8sOdbRnvtcTZv-UpHFK5egKL4QaNYiGwbDWxUwUgytm8eQt0ozjg2BZnQ6T_cZLfp1g78OegmK3d35QIEP0ShXKq1O5Qh815MaCzH8bD20pWgFHLlSgtjYdDiMo2TbsK-aKoVmRIv8chqOe1F7qWCHgsWJ8JSpqxaaBKq-8lt9uf8suexqGplGLnpJAoVl0qJ8DKZsz7-iz4dbMcJyRUYtNtvCkFJwvlxW-5VoUbaMZNmLv_-evig7zqrElVNX5vABQYg4MD4Ig6D9YsUyHDAAUvBd-MlLhTAAkdPsPLgByLewJZTxjAmlcrDAASCRwAd3cD5wEepeXvoHVSk4wvE9jxlGmDrgFGVVmyHMVEhdiqB_FjtGPYNItRVM8weyZTo-GR9v8usM5A_XsMk7wABq81Ws6B1FsoYppf9rcPiw_c4mJ_NTTDpdE5pks5NKFGuFD_vMAvRXJDpJ5i7bheEdyaLPftiE-D5yyNFtbxQ706Cr9aziPA92LQkIirE_Topw-dVfxqR8JtHrXx7IpnhOEMacaKM8dOad3K_v5ZoeKEkpiGGeZzMls41hA8CCMgnEmBuMGf21tVabIGLqv1VWNIG3N-9U8zuTIyZXTZjsg4sl5Cz4nezKHYer8xI1aL3vqzpQBIk0EUIIph6n9yxRpIZHI1YO8kfMTgx1sO_gYeqbfwqz1sT-Fsxp5rq22pzz66kDcNnLPehpKMQHTzs5aT_B0q6tBHIXiAMFlRGd0i3FnO_9cs78d7Pztz_cocVia7447b3vX7BqNg50-ESp0QXOOzKry1r9-Skf16WHuqfLwDXKocHD6qlQG4VlXgzXIiyzgXx8x86agdJNimz9wExbwYh_qQUq7TvY7LBxyP8ZP63UtK7RLv7kCPOqzSFKRMwdDJHxuLJG5xEUD5RNFpoOLq49341Qu5abdm2CIspG2I3E6R-T3ftomM12UErBj33FeLgoIlZdAGEdj7UIj9TCRoZJP4zaSbk3qfMYhxtAXYtl83AQHReXlDibH4xTHE8VaXCfGWFP-_nGhB_FbC7ADiwRIpauvnUJIImw_m4xdOcDz8rojBKPGypT4P5pgpnTZxTZcNMP2ktwQkhwxHig_A0j5ACqXVQu-ZbMpkEYygFdm8pfekdFQxm0j-ZzpLX0a5pgP4SRbE_JvlA1XVQ6b-KzqFMMCKwp0bEE8oYX6EH4Mw4JXJ0fP0te6ed6cM_iM6_hANJtISkAvj9gdpuyuUyX5JIerc9zEC6nsSfqHzgAt47llWf-iMVPnF64kdWkCFqQ3K4dPYTpBf3m0bXV5VL4q0iEiVlfvIAvLf94BlOTOgeK3VPRubu0EsA0-XCkHRv1SvuPRIuMJl4LDNIGwWB5FWG2J7f5wKvchqP3WHYjcsN9rvubUlj0WB-EXpzt3B1sKh4gW2uQFbCnV3kNm-YbczJLCFpSx9JIHTT714s-9IO-BT7R5rqQZEllnmaAmKR0y8FceRlbghOEBmhRX__4KnfOflpIUHR5s0eWPoidHUgahF1clv6a1y0ZywzQxZxRzNHhalI465BCrfhFKolEX_MkkHlGUfzX4SpGxtYmlxYxIEh0Urxj2cz8F7wZx2vGrTVDSNmR7hHrnoHsYq_ybhtpaCEIsCWOZA32WIVWOk-Pr8ndPVuiE_f9nT4vUSczJS2GCuTyVM185fRr0_fCk2UU5SWRZYaxfzaPNKVzxYMIA9alyTLp982rnkXCTSuy9HTwnXG2ak66VeIw6RkNAKpAh6t3cNpcArX3z_1HAgkL2PhS3Bprlu9xKeb-F9AfgNES5e_xzTcL550EChWNtHM5koi4yHzgea2DJR40tD0Fgguzc9Uoxn2DiKmrZsFBIN9ut2eTmdpuUgUBRzPcce_SPoY4yf4s2XCkDV9gaWmcSUyc5lEyJguLOgIsq6vt8xXqUj0pr-QeYCanbQDZlpE5Dawxk0fsXihtZxMuLnt6H56NwZ9MQxDH-_gW1TJfdalRc-Zp0tAnh-_sm8sFHq4vWzt_1n5EqBtAotAx9C3qCqLRWCsjAeTeFta_si2rOD5lR89VHCjra38x2-jT_DWHq9r8ogh0nHzIp2zVRsa6w0YQVDdB4betZIOCMWhwywUyDhNeaSuXypnsq0Mm-eBRSn8wQ6leDZAv5yiqMT4rc8wNGVC4A4j5Oe-kpBaJk4pT70QEWu2wdQHxlaeGbDsF2OW4GyOqZz1qPFl_CdQaxhkSoxmOL9UsT9v-GqYcEBPBd1yGdpzQfXwLABr8VFrizw19vB0pPIbTBjZGHY0euMVyP01pWlzB7M3Tu-Q9xUxZr8i65EQ1UrPj_d8I2KlJR8ZmjZZQYe0sFJjim8gntvwx1wCWq5XekDjr85hf0Ry-Rc3N1peWUgaxmHC4FU6wOPNMBo5ghP7477yFyqobNYVZqSWnmcjn-vFrB5lKxG6pleqKQwfaljiqDjFPl_MXgevZgGY_6XO72CDchogrybCmrw-dgyTig5JhsLGSCi2fYng9unvsJPdYvST5AWUHiov1UDcWwMFj-yi5KRrelngOA-7fiaO8DvtZUlAZjCxdwBB2wKxO74jSW3Bepe-guIWSzX2uLC48UYCBovVHTTmu-TPifjHlHhL76u08xSm1dB7usBuQduttSm4oYa9dOjcOKFLhl5tv2Iz7bUshLH7mAn6Db8jA1VD2CqAh5V5JNmPgGlCbAwGvng8szbLZgg7I3XNAeZ7Q3lZ7ixVdr-OhEsVAroyAuEPL0GiWT3Wa1ldGw9WBSEebPyhWyJiUQMWW5IcmWG2EYBlxVL455L2DNAHLQu85i6PViBcr3iNl-ZVQsXkOCAWfJBoadcibabqQGs_IqWjTqf-0B68dk2alSavnToCOl5k_Fvj3MC02vkOkQpRRC3v-9a8GscEtoQ20s6PU6aAkk0II_16xEPxEm7QnvSwsYu6PpN9U9KNMDko6wdi1f0ESKUZ85lL1KFsv7caPTvDBMhTkSniwp2jFybnlUXoqCRKLEfwbAHTaMbE3swsc-piJr24TopXcRy0EjoWn-LxazDmDRe242i38cwVGdXtkWGvco2bP17WHoVXe2SEsENbn51omCepjGBPVriMg1FmjkVgPEIhSlknLB8pwC6xK8LKMdaYQyCTXnm0XrJqWTSyRgZpH__mIaeqS4ZUPyXkSzaBcAKdb0sBAxNcS4C5js96dVTX3vMR0NJDmYweA; ASP.NET_SessionId=pc3agvnrcjvuksibhxv4w212; AWSALBTG=2YWK8fRyd6dtPLt5aZut/vM+mHdK645JDbBTe4PTzmhUZwGgD6uqV4mgHvIehepjQgRhEXKQ9aPmVC3KdmUbfzacCYSJtahWdIVFnxvhyog+OpNh1S1bE4ZAkMEN0b+bLckRb2UemYk6LTpP6wZdhKKKdj7l819TWO8QYiww94xDvSXBNVA; AWSALBTGCORS=2YWK8fRyd6dtPLt5aZut/vM+mHdK645JDbBTe4PTzmhUZwGgD6uqV4mgHvIehepjQgRhEXKQ9aPmVC3KdmUbfzacCYSJtahWdIVFnxvhyog+OpNh1S1bE4ZAkMEN0b+bLckRb2UemYk6LTpP6wZdhKKKdj7l819TWO8QYiww94xDvSXBNVA; PHPSESSID=2ldhjl4eccnkaln7auj71jlih1; Session=ed3aa2d0-543d-4ef2-b25c-e7b3d6b4e13f; _vis_opt_s=7%7C; _vis_opt_test_cookie=1; _vwo_ds=3%3At_0%2Ca_0%3A0%241707245738%3A99.19457355%3A%3A63_0%2C62_0%2C55_0%2C54_0%2C53_0%2C50_0%2C24_0%3A39_0%2C4_0%2C3_0%3A0; _vwo_uuid=D5BBB500A83CE588C0A1D2666B259D68E; _vwo_uuid_v2=D5BBB500A83CE588C0A1D2666B259D68E|c5b682c6429dfd30cdf18bb3d0b6e789; aapcCartCount=0; access_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IkhOUmluN082OVdEeGpfN2hFc1VTdjdxZ013ZllheFdaWkFEVzJFS1dNQkEiLCJ0eXAiOiJKV1QifQ.eyJ1c2VybmFtZSI6ImFtYTMzNkBjYXNlLmVkdSIsInN1YiI6IjU1YjgyYzQxLWViZGEtNGM1Ni1hNmUwLWVkMDI5MWM5NDY3MSIsImlzRW1haWxCb29sZWFuIjp0cnVlLCJyZXF1aXJlTWlncmF0aW9uIjpmYWxzZSwibWVtYmVySWQiOjIyMDE5MDksInZlcmlmaWNhdGlvbkVtYWlsIjoiYW1hMzM2QGNhc2UuZWR1IiwibmFtZSI6IkthbmkgQWhtZWQiLCJnaXZlbl9uYW1lIjoiS2FuaSIsImZhbWlseV9uYW1lIjoiQWhtZWQiLCJ0aWQiOiJmZDc4OTZmMC1kODJkLTRlODgtYWY0Mi03NjQzM2ViMjMyZjQiLCJpc0ZvcmdvdFBhc3N3b3JkIjpmYWxzZSwibm9uY2UiOiI2Mzg0Nzg3NzU3NDk2NDE1MjcuWVdZeFlUSXpaamN0WWpjNU15MDBZV0ZpTFRnM05qSXRNMk15T1RjeE1HSXdPV05qTW1SbE4yVmhNMkl0TVRFek15MDBaV1ZpTFRrMllUVXRNamN3WXpBNE4yRXpOV1U0Iiwic2NwIjoidGFzay5yZWFkIiwiYXpwIjoiMzEzY2Q4ZjQtMGFlYS00YmJmLTkzYjEtMTQ3NmM1MDY3NTM4IiwidmVyIjoiMS4wIiwiaWF0IjoxNzEyMjgwNzc4LCJhdWQiOiIzOGJlM2VkYi1mOWY0LTQ2ODAtYjBiZS05YzA2YjIzMWRhMTIiLCJleHAiOjE3MTIzNjcxNzgsImlzcyI6Imh0dHBzOi8vYWFwY2xvZ2luLmIyY2xvZ2luLmNvbS9mZDc4OTZmMC1kODJkLTRlODgtYWY0Mi03NjQzM2ViMjMyZjQvdjIuMC8iLCJuYmYiOjE3MTIyODA3Nzh9.I9-BoEjAEpeYGqMp-iCjSF8GfuaG6gD1KTekc-CG21st3hTdzDAyEI4EqWSiY1DEC1udhwwV8e5m5RtGBhvtQvvkuNBX-vzvDZeP8P98CuccBmrDRav5IvjU-TrKVTBvlT4ry-34E03fMCN5RJ5rp6eJc2ygQDQ81edKWC8CzGhwe2xoxHX2WlMHoz3TZOh_t9swT4v7egSFyHhrz6zZCcbFz7_IX4USr8IACGpKbBvK2qHpcGyAzQ1rARxOlt6ZsbyMGIQMYooNQmCmGHOb3ZvoahsyJl56kcXVFs7rp_lKaJnghOkLEoUcZObKbgKGOqH6xMhJUo8woY64l38M_A; bbChapterName=; helloBar=closed; helloBarLoggedIn=closed; intercom-device-id-zbytus9c=7f7fe62f-51db-4fb1-ac3c-fb05bc7ae0bd; intercom-id-zbytus9c=be63630a-ebb0-4bca-b8be-bfbb4b023920; intercom-session-zbytus9c=; mType=; submenuheader=-1c; tracker_device=b7166150-3836-4a21-8ebd-f3d0183a9dd3; uid=02201909; xf_session=jSTi0bwHzlNF_9fpmrfFvf4t8HL0KWRT'
}

# from CPT codes from /Users/kani/PycharmProjects/Hospital_Price_Transparency_Project/CPT_CODES/cpt_codes.txt
with open("/data-cleaning-pipeline-generated-data/CPT_CODES/cpt_codes_2.txt", 'r') as file:
    cpt_codes = file.read().splitlines()
    # counter for the number of diagnosis codes found
    total_diagnosis_codes = 0

    for cpt_code in cpt_codes:
        logging.info(f"Processing CPT code: {cpt_code}")
        print("--------------------------------------------")

        # Initial payload with no charval value
        payload = f'charval=&code={cpt_code}&type=coder_page'

        # Initial request to get the list of letters
        response = requests.post(url, headers=headers, data=payload, verify=False)

        # Dictionary to hold all code-description pairs
        all_code_descriptions = {}

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            class_to_extract = "pb_w"
            div = soup.find('div', class_=class_to_extract)
            if not div:
                # If no data is found, log an error and continue to the next CPT code
                logging.error(f"No data found for CPT code: {cpt_code}")
                continue
            # otherwise, extract the letters from the div
            extracted_letters = div.text.strip().split("\n")

            for extracted_letter in extracted_letters:
                print(extracted_letter)
                print("--------------------------------------------")
                payload = f'charval={extracted_letter}&code={cpt_code}&type=coder_page'
                response = requests.post(url, headers=headers, data=payload, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    second_class_to_extract = "points_table_scrollbar"
                    table_tbody = soup.find('tbody', class_=second_class_to_extract)
                    if table_tbody:
                        td_elements = table_tbody.find_all('td')
                        # Iterate over td elements and skip every second element
                        for index, td in enumerate(td_elements):
                            if index % 2 == 0:  # Check if the index is even
                                code = td.text.strip()
                                description = td.find_next('td').text.strip()
                                all_code_descriptions[code] = description
                                logging.info(f"Processing code: {code}")
                                total_diagnosis_codes += 1
                    else:
                        print(f"No data found for letter: {extracted_letter}")
                else:
                    print(f"Failed to retrieve data for letter: {extracted_letter}")
        else:
            print("Initial request failed.")
        pwd = os.getcwd()
        output_directory = os.path.join(pwd, "CODE_MAPPINGS_2")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file = os.path.join(output_directory, f"{cpt_code}_code_mappings.csv")

        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Diagnosis Code", "Description"])
            for code, description in all_code_descriptions.items():
                csvwriter.writerow([code, description])
        print("CSV file created successfully.")

logging.info("All Diagnosis codes processed and extracted.")
logging.info(f"Total diagnosis codes found: {total_diagnosis_codes}")