import yfinance as yf
import pandas as pd
import random

# Fetch historical price data for stocks
def fetch_data(symbols):
    return yf.download(symbols, start="2022-01-01", end="2023-01-01")['Close']

# Compute moving averages
def compute_moving_averages(data, short_window, long_window):
    sma_short = data.rolling(window=short_window, min_periods=1).mean()
    sma_long = data.rolling(window=long_window, min_periods=1).mean()
    return sma_short, sma_long

# Identify buy/sell signals based on SMA crossover
def identify_signals(data, sma_short, sma_long):
    buy_signals = (sma_short > sma_long) & (sma_short.shift(1) <= sma_long.shift(1))
    sell_signals = (sma_short < sma_long) & (sma_short.shift(1) >= sma_long.shift(1))
    return buy_signals, sell_signals

# Main portfolio and stock data
sp500_stocks = ['AAPL', 'MSFT', 'GOOGL', 'FB', 'AMZN']
historical_data = fetch_data(sp500_stocks)

# Calculate moving averages
sma_short, sma_long = compute_moving_averages(historical_data, short_window=40, long_window=100)

# Calculate buy/sell signals
buy_signals, sell_signals = identify_signals(historical_data, sma_short, sma_long)

# Assuming you have historical purchase data and current prices
portfolio_data = {
    'Symbol': ['AAPL', 'MSFT', 'GOOGL'],
    'Purchase Price': [150, 220, 1400],
    'Shares': [10, 15, 5],
    'Current Price': [140, 230, 1350]  # Manually input current prices
}
portfolio = pd.DataFrame(portfolio_data)
portfolio['Value Change'] = (portfolio['Current Price'] - portfolio['Purchase Price']) * portfolio['Shares']

# Filter for losses
loss_stocks = portfolio[portfolio['Value Change'] < 0]
print("Stocks to consider for tax-loss harvesting:")
print(loss_stocks)

# Analyze signals for stocks considered for tax-loss harvesting
print("\nBest timing based on moving averages:")
for symbol in loss_stocks['Symbol']:
    if sell_signals[symbol].iloc[-1]:  # Check the latest available signal
        print(f"Sell {symbol} now based on moving average crossover.")
    else:
        print(f"Hold {symbol} as the conditions are not favorable for selling based on moving averages.")

# Suggest replacement stocks randomly from the S&P 500 list
print("\nSuggested replacement stocks:")
for index, row in loss_stocks.iterrows():
    possible_replacements = [s for s in sp500_stocks if s != row['Symbol']]
    replacement = random.choice(possible_replacements)
    print(f"Replace {row['Symbol']} with {replacement}")
