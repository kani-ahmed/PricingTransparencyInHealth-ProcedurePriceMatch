import requests
from bs4 import BeautifulSoup

# URLs for CPT and HCPCS codes
cpt_url = "https://www.aapc.com/codes/cpt-codes/20610"
#hcpcs_url = "https://www.aapc.com/codes/hcpcs-codes/Q0114"
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
    'Cookie': 'Session=c18f3af0-13ab-407a-b842-62d44640916e; aapcCartCount=0; .ASPXANONYMOUS=cfAZrYiqosuppjWWAsKnuGDzDVuI_f2Ool0Ykw6K4EJU7XwR3_XO0oWKbEmJe6AQ0kU6xzH2eWh7o5sV3PGRkMVfeexQF2HaPhPONn6xjZzRiWbzEbf-7c4vc35G43y7GB7i3g2; ASP.NET_SessionId=xs3ngcgclnz3rifms3yr2jxi; AWSALBTG=2audZ2VB7Iqu+qH6LVCHIEM+6Nzo3yEbElKK2OiSa3pnCPmwveVqMFns4UMOuh9mXU5jVEH7TAW+ZUH7ooGTxklksP5Fwl87PdwtVO7u7nH5uqIHGx2r+OCdmvc/+DhQhRiXGbgS0wezNh1D/uAt/6z80tdwNKsub/CC+xPZSCfHOJd8JdU=; AWSALBTGCORS=2audZ2VB7Iqu+qH6LVCHIEM+6Nzo3yEbElKK2OiSa3pnCPmwveVqMFns4UMOuh9mXU5jVEH7TAW+ZUH7ooGTxklksP5Fwl87PdwtVO7u7nH5uqIHGx2r+OCdmvc/+DhQhRiXGbgS0wezNh1D/uAt/6z80tdwNKsub/CC+xPZSCfHOJd8JdU=; PHPSESSID=inb6klo4i8ufu7hksovaroudr2'
}


def fetch_description(url, container_id):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.find(id=container_id)
    if container:
        description_p = container.find('p')
        if description_p:
            return description_p.get_text(strip=True)
        else:
            return "Paragraph not found in container."
    else:
        return "Container ID not found."


# Fetch and print description for CPT code
cpt_description = fetch_description(cpt_url, "cpt_layterms")
print("CPT Description:", cpt_description)

# Fetch and print description for HCPCS code
#hcpcs_description = fetch_description(hcpcs_url, "hcpcs_layterm")
#print("HCPCS Description:", hcpcs_description)
