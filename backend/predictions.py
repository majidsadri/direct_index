import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

# Fetch historical stock data
ticker = "NVDA"
data = yf.download(ticker, start="2023-01-01", end="2024-02-20")

# Prepare the data
data = data[['Close']].copy()  # Make a copy to avoid SettingWithCopyWarning
data['Day'] = data.index.dayofyear
data['Year'] = data.index.year
data['Target'] = data['Close'].shift(-1)  # Shift closing prices to get the next day as target
data.dropna(inplace=True)  # Drop rows with NaN values, especially the last row

# Split data into features (X) and target (y)
X = data[['Day', 'Year']]
y = data['Target']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the testing set
predictions = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Predict the next day's closing price (this is a placeholder; adjust as needed)
next_day = np.array([[1, 2024]])  # Replace with actual future dates
predicted_price = model.predict(next_day)
print(f"Predicted next day's price: ${predicted_price[0]:.2f}")
