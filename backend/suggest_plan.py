import yfinance as yf
import numpy as np
import pandas as pd

# Define a simplified list of stock symbols (representing a portion of an index)
stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']
exclusions = ['TSLA']  # Exclude specific stocks for customization (e.g., sustainability)

# Apply exclusions
stocks = [stock for stock in stocks if stock not in exclusions]

# Define an initial portfolio (stock symbol: quantity)
portfolio = {'AAPL': 10, 'MSFT': 8, 'AMZN': 2}  # Example: pre-existing portfolio

# Fetch historical data for the stocks
start_date = "2023-01-01"
end_date = "2023-12-31"
data = yf.download(stocks, start=start_date, end=end_date)['Close']

# Ensure all data is fetched; if any stock has missing data, it's dropped
data = data.dropna(axis=1)

# Filter portfolio to include only stocks present in the data
portfolio_filtered = {stock: portfolio[stock] for stock in portfolio if stock in data.columns}

# Convert the filtered portfolio to a Series aligned with the data columns
portfolio_series = pd.Series(portfolio_filtered).reindex(data.columns, fill_value=0)

# Calculate daily returns for the portfolio and the index
portfolio_returns = data.pct_change().fillna(0).dot(portfolio_series)
index_returns = data.pct_change().mean(axis=1)  # Simulated index returns as average returns of constituents

# Calculate the correlation between portfolio and index returns
correlation = portfolio_returns.corr(index_returns)
print(f"Correlation with the index: {correlation:.2f}")

# Define a loss threshold for making sell recommendations
loss_threshold = -0.10  # -10%

# Fetch current stock prices for buy/sell decisions
current_prices = yf.download(stocks, period="1d")['Close'].iloc[-1]

# Determine buy and sell recommendations
recommendations = []

for stock in stocks:
    if stock in portfolio:
        purchase_price = data.iloc[0][stock]  # Assume purchase at the start date for simplicity
        current_price = current_prices[stock]
        loss = (current_price - purchase_price) / purchase_price

        if loss < loss_threshold:
            recommendations.append((stock, 'SELL', portfolio[stock], f"Loss: {loss*100:.2f}%"))
    else:
        recommendations.append((stock, 'BUY', 'N/A', 'Not in portfolio'))

# Display recommendations
print("\nRecommendations:")
for rec in recommendations:
    print(f"{rec[0]}: {rec[1]} {rec[2]} shares ({rec[3]})")
