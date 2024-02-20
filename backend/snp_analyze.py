import pandas as pd
import yfinance as yf

def get_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url, attrs={'id': 'constituents'})[0]
    symbols = sp500_table['Symbol']
    return symbols

# Fetch S&P 500 symbols
sp500_symbols = get_sp500_symbols()

# Initialize a list to hold EPS data
eps_data = []

# Loop through each symbol and fetch EPS TTM
for symbol in sp500_symbols:
    try:
        stock = yf.Ticker(symbol)
        eps_ttm = stock.info.get('trailingEps', None)
        # Only add to list if EPS data is available
        if eps_ttm is not None:
            eps_data.append((symbol, eps_ttm))
    except Exception as e:
        print(f"Could not fetch data for {symbol}: {e}")

# Convert the EPS data to a DataFrame
eps_df = pd.DataFrame(eps_data, columns=['Symbol', 'EPS TTM'])

# Sort the DataFrame by EPS TTM in descending order and select the top 20
top_20_eps = eps_df.sort_values(by='EPS TTM', ascending=False).head(20)

print(top_20_eps)
