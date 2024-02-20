import yfinance as yf
import numpy as np
import pandas as pd

# Fetch S&P 500 Index data
sp500_data = yf.download('^GSPC', start="2023-01-01", end="2023-12-31")['Close']

# Define a larger set of stocks to consider
all_stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'TSLA', 'BRK-B', 'JPM', 'V']

# Fetch historical data for these stocks
all_data = yf.download(all_stocks, start="2023-01-01", end="2023-12-31")['Close']

# Calculate daily returns for all stocks and the S&P 500
daily_returns_all = all_data.pct_change()
daily_returns_sp500 = sp500_data.pct_change()

# Calculate correlations with S&P 500
correlations = daily_returns_all.apply(lambda x: x.corr(daily_returns_sp500))

# Select top N stocks with highest correlation to S&P 500
N = 5
selected_stocks = correlations.nlargest(N).index.tolist()

# Fetch historical data for selected stocks
data = all_data[selected_stocks]

# Continue with your existing code but for the selected stocks
initial_weights = np.array([1/N] * N)  # Assuming equal weights for simplicity

# Total investment amount
total_investment = 10000

# Calculate daily returns
daily_returns = data.pct_change()

# Calculate expected returns and covariance matrix for the portfolio
expected_returns = daily_returns.mean()
covariance_matrix = daily_returns.cov()

# Portfolio optimization as per your existing strategy
risk_tolerance = 0.5  # Scale from 0 (risk-averse) to 1 (risk-tolerant)
volatility = np.sqrt(np.diag(covariance_matrix))
risk_adjusted_weights = 1 / volatility
risk_adjusted_weights /= risk_adjusted_weights.sum()  # Normalize weights

# Combine initial weights with risk-adjusted weights based on risk tolerance
final_weights = (1 - risk_tolerance) * initial_weights + risk_tolerance * risk_adjusted_weights

# Adjust final weights to ensure they sum to 1
final_weights /= final_weights.sum()

# Calculate the number of shares to buy for each stock
latest_prices = data.iloc[-1]
shares_to_buy = total_investment * final_weights / latest_prices

# Print investment plan
print("\nInvestment Plan:")
for stock, shares in zip(selected_stocks, shares_to_buy):
    print(f"{stock}: Buy {shares:.2f} shares")

# Note: This is a simplified example. Real-world applications should include more comprehensive risk management,
# factor in transaction costs, handle rebalancing, and consider tax implications.
