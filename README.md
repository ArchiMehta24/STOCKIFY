# STOCKIFY
A web application to analyze stocks with news sentiment, technical indicators, and AI-powered predictions

## Installation
### Cloning the repository:

### Installing dependencies:
Run `pip install -r requirements.txt`
### Starting the server:
Run `./run_app.sh`.
Open http://localhost:5000 to view it in the browser.

## Features
### News Sentiment Analysis
- Fetches stock-related news and analyzes sentiment (Positive/Negative/Neutral) using NLTK.
- Displays articles with scores and links.

### Technical Indicators
- Interactive charts for Bollinger Bands, RSI, MACD, and Volume Analysis (generated with Plotly).
- Supports preloaded stocks (AAPL, RELIANCE.NS).

### Candlestick Patterns
- Visualize Open-High-Low-Close (OHLC) data with dynamic candlestick charts.

### Stock Price Prediction
- LSTM model predicts future stock prices based on historical data.
- Simulates investment returns for user-defined amounts and durations.

### Chatbot
- AI-powered chatbot (Groq API) answers stock-related queries.

## Developer
### This Project was built by

- Archi Mehta
