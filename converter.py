import pandas as pd

# Read currency.csv, all_indices_data.csv, and world_indices.csv files
currency_df = pd.read_csv('currency.csv')
all_indices_data_df = pd.read_csv('all_indices_data.csv')
world_indices_df = pd.read_csv('world_indices.csv')

# Convert date to year
all_indices_data_df['year'] = pd.to_datetime(all_indices_data_df['date']).dt.year

# Merge world_indices_df with all_indices_data_df based on the ticker symbol
merged_df = pd.merge(all_indices_data_df, world_indices_df, on='ticker', how='inner')

# Function to convert open prices to USD based on the original currency
def convert_to_usd(row):
    year = row['year']
    open_price = row['open']
    high_price = row['high']
    low_price = row['low']
    close_price = row['close']
    original_currency = row['currency']

    usd_open = None
    usd_high = None
    usd_low = None
    usd_close = None

    if year in currency_df['Year'].values:
        currency_rates = currency_df[currency_df['Year'] == year].iloc[0]

        # Check if the original currency exists in the currency_rates
        if original_currency in currency_rates.index:
            exchange_rate = currency_rates[original_currency]

            # Convert to USD using the exchange rate
            usd_open = open_price * exchange_rate
            usd_high = high_price * exchange_rate
            usd_low = low_price * exchange_rate
            usd_close = close_price * exchange_rate
        else:
            print(f"Exchange rate not found for {original_currency} in year {year}")
    else:
        print(f"Year {year} not found in currency data")

    return pd.Series({
        'open_usd': usd_open,
        'high_usd': usd_high,
        'low_usd': usd_low,
        'close_usd': usd_close
    })

# Apply currency conversion to merged_df and add new columns
merged_df[['open_usd', 'high_usd', 'low_usd', 'close_usd']] = merged_df.apply(convert_to_usd, axis=1)

# Drop the 'currency' and 'name' column as these are not needed in this table.
merged_df = merged_df.drop(columns=['currency', 'name'])

# Save the updated dataframe with USD equivalent values
merged_df.to_csv('all_indices_data_usd.csv', index=False)

print("Currency conversion to USD completed and saved to all_indices_data_usd.csv")