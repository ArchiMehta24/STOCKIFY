# stock_predictions.py
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import os

def predict_stock_price(stock, data, duration_days=365, investment_amount=1000):
    model_file = f"{stock}_lstm_model.h5"
    
    if not os.path.exists(model_file):
        return f"Model for {stock} not found. Please train it first."

    # Load trained model
    model = load_model(model_file)

    # Preprocess data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data["Close"].values.reshape(-1, 1))

    # Prepare last sequence
    seq_length = 60
    last_sequence = scaled_data[-seq_length:]
    predictions = []
    
    for _ in range(duration_days):
        last_sequence_reshaped = last_sequence.reshape(1, seq_length, 1)
        pred = model.predict(last_sequence_reshaped)
        predictions.append(pred[0, 0])
        last_sequence = np.append(last_sequence[1:], pred).reshape(seq_length, 1)

    # Transform back to original scale
    predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    # Generate future dates
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=duration_days+1)[1:]

    # Calculate returns and volatility
    daily_returns = np.diff(predicted_prices) / predicted_prices[:-1]
    annualized_return = np.mean(daily_returns) * 252  # 252 trading days
    annualized_volatility = np.std(daily_returns) * np.sqrt(252)
    
    # Calculate expected investment value
    initial_price = predicted_prices[0]
    final_price = predicted_prices[-1]
    expected_value = investment_amount * (final_price / initial_price)
    
    # Create Plotly chart
    trace_actual = go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Actual Prices")
    trace_predicted = go.Scatter(x=future_dates, y=predicted_prices, mode="lines", name="Predicted Prices")

    # Create metrics display
    metrics_html = f"""
    <div class="metrics-container" style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h4>Investment Analysis</h4>
        <p><strong>Initial Investment:</strong> ₹{investment_amount:,.2f}</p>
        <p><strong>Expected Value:</strong> ₹{expected_value:,.2f}</p>
        <p><strong>Expected Return:</strong> {(final_price/initial_price - 1)*100:.2f}%</p>
        <p><strong>Annualized Return:</strong> {annualized_return*100:.2f}%</p>
        <p><strong>Annualized Volatility:</strong> {annualized_volatility*100:.2f}%</p>
    </div>
    """

    fig = go.Figure([trace_actual, trace_predicted])
    fig.update_layout(
        title=f"{stock} Stock Price Prediction (Next {duration_days} Days)",
        xaxis_title="Date",
        yaxis_title="Stock Price",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),
        xaxis=dict(showgrid=True, gridcolor="lightgray"),
        yaxis=dict(showgrid=True, gridcolor="lightgray")
    )

    return metrics_html + pio.to_html(fig, full_html=False)