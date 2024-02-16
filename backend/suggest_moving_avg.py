import yfinance as yf
import pandas as pd

def fetch_data(stock, start_date, end_date):
    """Fetch historical data for a given stock."""
    data = yf.download(stock, start=start_date, end=end_date)
    return data

def calculate_moving_averages(data, short_window=50, long_window=400):
    """Calculate short-term and long-term moving averages."""
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

def identify_buy_signals(data):
    """Identify buy signals based on moving average crossovers."""
    # Shift the short MA to align its previous day's values with the current day's long MA
    data['Prev_Short_MA'] = data['Short_MA'].shift(1)
    data['Prev_Long_MA'] = data['Long_MA'].shift(1)
    
    # A buy signal occurs when the short MA crosses above the long MA
    buy_signals = data[(data['Short_MA'] > data['Long_MA']) & (data['Prev_Short_MA'] < data['Prev_Long_MA'])]
    return buy_signals

# List of stocks to analyze
stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']

# Define the start and end dates for historical data
start_date = '2023-01-01'
end_date = '2023-12-31'

# Iterate over each stock, analyze, and print buy signals
for stock in stocks:
    data = fetch_data(stock, start_date, end_date)
    data_with_moving_averages = calculate_moving_averages(data)
    print(data_with_moving_averages)
    buy_signals = identify_buy_signals(data_with_moving_averages)
    
    if not buy_signals.empty:
        print(f"Buy signals for {stock}:")
        print(buy_signals[['Short_MA', 'Long_MA']])
    else:
        print(f"No buy signals for {stock} in the given period.")
