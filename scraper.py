import pandas as pd
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

def get_index_details(index_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
    }
    soup = BeautifulSoup(requests.get(index_url, headers=headers).content, "html.parser")

    # Extract 'useful sentence' w/ region and currency inside.
    region_element = soup.find("div", class_="C($tertiaryColor) Fz(12px)")
    region = region_element.text.strip() if region_element else "N/A"

    return region

def extract_currency(sentence):
    # Extract currency code (assumes it's at the end of the sentence)
    parts = sentence.split('-')
    if len(parts) > 1:
        currency_part = parts[1].strip()
        currency_code = currency_part.split()[-1].strip()
        return currency_code
    return "N/A"

base_url = "https://finance.yahoo.com/quote/"
world_indices_url = "https://finance.yahoo.com/world-indices/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
}

soup = BeautifulSoup(requests.get(world_indices_url, headers=headers).content, "html.parser")

tickers = []
names = []
regions = []
currencies = []

for a in soup.select('a[data-test="quoteLink"]'):
    ticker = a.text
    name = a['title']
    index_url = base_url + ticker  # Construct the full URL for each index

    # Check if the ticker is already in the list
    if ticker not in tickers:
        tickers.append(ticker)
        names.append(name)

        # Get index details
        details = get_index_details(index_url)
        region = details.split('-')[0].strip()  # Extract region
        currency = extract_currency(details)  # Extract currency
        city_name = region.split(',')[0].strip()  # Extract city name from region

        currencies.append(currency)

# Create DataFrame from lists
df = pd.DataFrame({
    'ticker': tickers,
    'name': names,
    'currency': currencies
})

# Save DataFrame to CSV
df.to_csv('world_indices.csv', index=False)

# Print DataFrame
print(df)

