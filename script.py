import requests
from bs4 import BeautifulSoup
import json

def search_vst_plugins(query, base_urls, output_file='vst_data.json'):
    vst_data = []

    for base_url in base_urls:
        search_url = f'{base_url}/search?q={query}'

        # Send an HTTP GET request to the website
        response = requests.get(search_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract information about the VST plugins (adjust based on website structure)
            plugin_results = soup.find_all('div', class_='plugin-info')

            # Process and append the results to vst_data
            for result in plugin_results:
                plugin_name = result.find('h2', class_='plugin-name').text
                plugin_author = result.find('p', class_='plugin-author').text

                # Get the plugin details page URL
                plugin_details_url = result.find('a', class_='plugin-details')['href']
                price, price_drop = scrape_price_info(base_url + plugin_details_url)

                vst_entry = {
                    'name': plugin_name,
                    'author': plugin_author,
                    'price': price,
                    'price_drop': price_drop,
                    'url': base_url + plugin_details_url
                }

                vst_data.append(vst_entry)
        else:
            print(f"Failed to retrieve page from {base_url}. Status code: {response.status_code}")

    # Save the collected data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(vst_data, json_file, indent=2)

    print(f"Data saved to {output_file}")

def scrape_price_info(plugin_details_url):
    # Send an HTTP GET request to the plugin details page
    response = requests.get(plugin_details_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract price and price drop information (adjust based on website structure)
        price_element = soup.find('span', class_='plugin-price')
        price = price_element.text if price_element else "N/A"

        price_drop_element = soup.find('span', class_='price-drop')
        price_drop = price_drop_element.text if price_drop_element else "No Price Drop"

        return price, price_drop
    else:
        print(f"Failed to retrieve price info from {plugin_details_url}. Status code: {response.status_code}")
        return "N/A", "No Price Drop"

# Example usage:
search_query = 'synth'
base_urls = ['https://example1.com', 'https://example2.com', 'https://example3.com']

search_vst_plugins(search_query, base_urls)
