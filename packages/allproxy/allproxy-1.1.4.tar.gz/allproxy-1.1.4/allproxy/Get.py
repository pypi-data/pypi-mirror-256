import requests
from bs4 import BeautifulSoup
from tqdm import tqdm, trange
import threading
from packaging import version

current_version = "1.1.4"

response = requests.get('https://pypi.org/pypi/allproxy/json')
web_version = response.json()["info"]["version"]

if version.parse(web_version) > version.parse(current_version):
    print("Hey there! Please update to the new version of allproxy by using pip install --upgrade allproxy!")

working_proxies = []
progress_bar = tqdm(desc="Checking Proxies", unit="URL", position=0, leave=True)

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
    global working_proxies
    global progress_bar

    for full_url in urls:
        try:
            # Add 'http://' or 'https://' based on your needs
            full_url_with_protocol = 'http://' + full_url if not full_url.startswith('http') else full_url

            response = requests.get(full_url_with_protocol, timeout=5)
            if response.status_code == 200:
                working_proxies.append(full_url)

        except requests.RequestException as e:
            pass  # Handle exception if needed

        finally:
            # Update progress bar even if an exception occurs
            progress_bar.update()

def get_proxies():
    # Replace with the any URL you want to scrape
    website_url = 'https://free-proxy-list.net/'
    result = combine_and_store(website_url)

    if result:
        num_threads = len(result)  # Use as many threads as there are proxies

        # Split the list of proxies into chunks for parallel processing
        chunks = [result[i:i + 1] for i in range(0, len(result))]

        for _ in trange(num_threads, desc="Threads", position=1, leave=False):
            thread = threading.Thread(target=check_proxie_reachable, args=(chunks,))
            thread.start()
            thread.join()

        progress_bar.close()

        if working_proxies:
            return working_proxies
        else:
            print("No working proxies found.")
    else:
        print("Failed to retrieve the page or table not found.")