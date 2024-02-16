import yfinance as yf
import numpy as np
import pandas as pd

# Define a set of stocks and initial weights (e.g., mimicking an index)
stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']
initial_weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

# Total investment amount
total_investment = 10000

# Fetch historical data for these stocks
data = yf.download(stocks, start="2023-01-01", end="2023-12-31")['Close']

# Calculate daily returns
daily_returns = data.pct_change()

# Calculate expected returns and covariance matrix for the portfolio
expected_returns = daily_returns.mean()
covariance_matrix = daily_returns.cov()

# Portfolio optimization:
# For simplicity, we'll define a risk tolerance factor that adjusts the weights inversely based on their volatility.
# A more sophisticated approach would involve solving an optimization problem to find the optimal weights.
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
for stock, shares in shares_to_buy.items():
    print(f"{stock}: Buy {shares:.2f} shares")

# Note: This is a simplified example. Real-world applications should include more comprehensive risk management,
# factor in transaction costs, handle rebalancing, and consider tax implications.
