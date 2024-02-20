import yfinance as yf
import pandas as pd

def fetch_data(symbols, start_date, end_date):
    data = yf.download(symbols, start=start_date, end=end_date)
    if len(symbols) == 1:  # If only one symbol is fetched, ensure the DataFrame format is preserved
        data = data[['Adj Close']].rename(columns={'Adj Close': symbols[0]})
    else:
        data = data['Adj Close']
    return data


def calculate_correlations(stock_data, index_data):
    returns = stock_data.pct_change().apply(lambda x: x.fillna(0))
    index_returns = index_data.pct_change().fillna(0)
    correlations = returns.apply(lambda x: x.corr(index_returns))
    return correlations

def select_stocks(correlations, num_stocks=10):
    highest_correlations = correlations.nlargest(num_stocks)
    return highest_correlations

# Define the symbols for the S&P 500 index and a sample of S&P 500 stocks
index_symbol = '^GSPC'  # S&P 500 Index
stock_symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'BRK.B', 'JNJ', 'V', 'PG', 'UNH', 'MA', 'INTC', 'TSLA', 'JPM', 'XOM']

# Fetch historical data
start_date = '2023-01-01'
end_date = '2023-12-31'
# Fetch historical data for the S&P 500 index
index_data = fetch_data([index_symbol], start_date, end_date)[index_symbol]
stock_data = fetch_data(stock_symbols, start_date, end_date)

# Calculate correlations
correlations = calculate_correlations(stock_data, index_data)

# Select stocks for the portfolio
selected_stocks = select_stocks(correlations)
print(selected_stocks)
