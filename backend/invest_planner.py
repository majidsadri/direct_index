import yfinance as yf
import numpy as np
import pandas as pd

def fetch_sp500_symbols_and_sectors():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url, attrs={'id': 'constituents'})[0]
    symbols_sectors = sp500_table[['Symbol', 'GICS Sector']]
    return symbols_sectors.set_index('Symbol')

# Fetch S&P 500 symbols and their sectors
sp500_symbols_sectors = fetch_sp500_symbols_and_sectors()

# Fetch historical data for S&P 500 Index
index_symbol = '^GSPC'
sp500_index_data = yf.download(index_symbol, start="2023-01-01", end="2023-12-31")['Close']

# Calculate daily returns for the S&P 500
daily_returns_sp500 = sp500_index_data.pct_change()

# Fetch historical data for all S&P 500 stocks
all_symbols = sp500_symbols_sectors.index.tolist()
all_data = yf.download(all_symbols, start="2023-01-01", end="2023-12-31")['Close']

# Calculate daily returns for all stocks
daily_returns_all = all_data.pct_change()

# Calculate correlations with S&P 500
correlations = daily_returns_all.apply(lambda x: x.corr(daily_returns_sp500))

# Select top 20 stocks with highest correlation to S&P 500
top_20_stocks = correlations.nlargest(50).index.tolist()

# Fetch historical data for top 20 correlated stocks
data = all_data[top_20_stocks]

# Get GICS Sector for the selected stocks
selected_stocks_sectors = sp500_symbols_sectors.loc[top_20_stocks]

# Assuming equal weights for simplicity
initial_weights = np.array([1/50] * 50)

# Total investment amount
total_investment = 10000

# Calculate daily returns
daily_returns = data.pct_change()

# Calculate expected returns and covariance matrix for the portfolio
expected_returns = daily_returns.mean()
covariance_matrix = daily_returns.cov()

# Portfolio optimization as per your existing strategy
risk_tolerance = 0.5
volatility = np.sqrt(np.diag(covariance_matrix))
risk_adjusted_weights = 1 / volatility
risk_adjusted_weights /= risk_adjusted_weights.sum()

# Combine initial weights with risk-adjusted weights based on risk tolerance
final_weights = (1 - risk_tolerance) * initial_weights + risk_tolerance * risk_adjusted_weights

# Adjust final weights to ensure they sum to 1
final_weights /= final_weights.sum()

# Calculate the number of shares to buy for each stock
latest_prices = data.iloc[-1]
shares_to_buy = total_investment * final_weights / latest_prices


# Define the ANSI escape codes for yellow and reset
yellow = '\033[1;32m'
reset = '\033[0m'

# Print the investment plan header in yellow
print("\n")
print(f"{yellow}Investment Plan for a Total Investment of $10000:{reset}")
print("Based on S&P 500 correlation and adjusted for risk tolerance, the following is the recommended purchase plan:")
print("\n")
for stock, shares in zip(top_20_stocks, shares_to_buy):
    sector = selected_stocks_sectors.loc[stock, 'GICS Sector']
    # Print stock symbols in yellow
    print(f"{yellow}{stock}{reset} ({sector}): Buy {shares:.2f} shares")

print("\nThis plan aims to closely mirror the S&P 500 trends while considering the individual stock volatilities to optimize the risk-reward ratio of the investment.")
