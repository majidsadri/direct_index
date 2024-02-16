import yfinance as yf
import numpy as np
import pandas as pd

# Initial setup: stocks, weights, and total investment
stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']
initial_weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
total_investment = 10000

# Mock purchase prices for simplicity. In a real scenario, you'd have actual purchase data.
purchase_prices = {'AAPL': 150, 'MSFT': 250, 'AMZN': 3100, 'GOOGL': 2800, 'META': 350}
purchase_quantities = {'AAPL': 10, 'MSFT': 8, 'AMZN': 2, 'GOOGL': 2, 'META': 5}

# Define a loss threshold (e.g., -10%)
loss_threshold = -0.10

# Fetch current stock prices
data = yf.download(stocks, period="1d")['Close'].iloc[-1]

# Recommendations
buy_recommendations = []
sell_recommendations = []

# Calculate current value and losses
for stock in stocks:
    current_price = data[stock]
    purchase_price = purchase_prices[stock]
    quantity = purchase_quantities[stock]
    current_value = current_price * quantity
    purchase_value = purchase_price * quantity
    loss_percentage = (current_price - purchase_price) / purchase_price

    # Make sell recommendations based on the loss threshold
    if loss_percentage < loss_threshold:
        sell_recommendations.append((stock, "SELL", quantity, f"Loss: {loss_percentage*100:.2f}%"))
    else:
        # Make buy recommendations based on the risk-adjusted weights (for simplicity, assuming more investment)
        # In a real application, you'd also consider the available budget, investment strategy adjustments, etc.
        buy_recommendations.append((stock, "BUY", f"Current Loss/Gain: {loss_percentage*100:.2f}%"))

# Print recommendations
print("Sell Recommendations:")
for rec in sell_recommendations:
    print(f"{rec[0]}: {rec[1]} {rec[2]} shares ({rec[3]})")

print("\nBuy Recommendations:")
for rec in buy_recommendations:
    print(f"{rec[0]}: {rec[1]} ({rec[2]})")

