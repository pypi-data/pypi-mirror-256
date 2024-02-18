import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import threading

working = []

def combine_and_store(url):
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table with specified headers
            table = soup.find('table')

            if table:
                combined_data = []

                # Extract headers
                headers = [th.text.strip() for th in table.find_all('th')]
                header_indexes = [headers.index('IP Address'), headers.index('Port'), headers.index('Https')]

                # Extract data rows
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip the first row if it contains headers
                    row_data = [td.text.strip() for td in row.find_all('td')]

                    if row_data:
                        # Extract relevant data based on header indexes
                        extracted_data = [row_data[i] for i in header_indexes]

                        # Check if Https is "no" and combine IP and Port
                        if extracted_data[2].lower() == 'no':
                            combined_data.append(extracted_data[0] + ':' + extracted_data[1])

                return combined_data

            else:
                return None  # Return None if table not found

        else:
            return None  # Return None if response status code is not 200

    except requests.RequestException as e:
        return None  # Return None if an error occurs

def check_proxie_reachable(urls):
    def check_url(full_url):
        try:
            # Add 'http://' or 'https://' based on your needs
            full_url_with_protocol = 'http://' + full_url if not full_url.startswith('http') else full_url

            response = requests.get(full_url_with_protocol, timeout=5)
            if response.status_code == 200:
                working.append(full_url)
            return full_url_with_protocol, response.status_code
        except requests.RequestException as e:
            return full_url_with_protocol, e

    threads = []
    for full_url in urls:
        thread = threading.Thread(target=lambda: check_url(full_url))
        threads.append(thread)
        thread.start()

    for thread in tqdm(threads, desc="Checking Proxies", total=len(threads)):
        thread.join()

    return working

def get_proxies():
    # Replace with the any URL you want to scrape
    website_url = 'https://free-proxy-list.net/'
    result = combine_and_store(website_url)
    if result:
        working_proxies = check_proxie_reachable(result)

        if working_proxies:
            return working_proxies
        else:
            print("No working proxies found.")
    else:
        print("Failed to retrieve the page or table not found.")