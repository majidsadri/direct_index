from flask import Flask, request, render_template_string
import yfinance as yf
import numpy as np
import pandas as pd

app = Flask(__name__)

HTML = '''
<!doctype html>
<html>
<head><title>Investment Planner</title></head>
<body>
    <h2>Investment Planner</h2>
    <form method="post">
        Total Investment ($): <input type="text" name="total_investment" value="{{total_investment}}"><br>
        Risk Tolerance (0 to 1): <input type="text" name="risk_tolerance" value="{{risk_tolerance}}"><br>
        <input type="submit" value="Generate Investment Plan">
    </form>
    {% if shares_to_buy %}
        <h3>Investment Plan:</h3>
        <ul>
        {% for stock, shares in shares_to_buy.items() %}
            <li>{{ stock }}: Buy {{ shares }} shares</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def investment_planner():
    total_investment = 10000  # Default investment amount
    risk_tolerance = 0.5  # Default risk tolerance
    shares_to_buy = {}

    if request.method == 'POST':
        total_investment = float(request.form.get('total_investment', 10000))
        risk_tolerance = float(request.form.get('risk_tolerance', 0.5))

        # Your original investment planning code adapted for Flask
        stocks = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']
        initial_weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

        data = yf.download(stocks, start="2023-01-01", end="2023-12-31")['Close']
        daily_returns = data.pct_change()
        expected_returns = daily_returns.mean()
        covariance_matrix = daily_returns.cov()

        volatility = np.sqrt(np.diag(covariance_matrix))
        risk_adjusted_weights = 1 / volatility
        risk_adjusted_weights /= risk_adjusted_weights.sum()

        final_weights = (1 - risk_tolerance) * initial_weights + risk_tolerance * risk_adjusted_weights
        final_weights /= final_weights.sum()

        latest_prices = data.iloc[-1]
        shares_to_buy = (total_investment * final_weights / latest_prices).to_dict()

    return render_template_string(HTML, total_investment=total_investment, risk_tolerance=risk_tolerance, shares_to_buy=shares_to_buy)

if __name__ == '__main__':
    app.run(debug=True)
