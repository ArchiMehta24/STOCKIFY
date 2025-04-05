#app.py
from flask import Flask, render_template, request, jsonify
import pandas as pd
from stock_analysis import get_technical_indicators, get_candlestick_chart
from news_scraper import fetch_news
from sentiment_analysis import analyze_news
from stock_prediction import predict_stock_price  # Importing the new prediction function
from chatbot import chatbot_response  # Import chatbot logic

app = Flask(__name__)

# Load stock data
aapl_data = pd.read_csv("AAPL_stock_data.csv", parse_dates=["Date"], index_col="Date")
reliance_data = pd.read_csv("RELIANCE.NS_stock_data.csv", parse_dates=["Date"], index_col="Date")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_news")
def get_news():
    stock_name = request.args.get("stock")
    if not stock_name:
        return jsonify({"error": "Stock name is required!"}), 400

    articles = fetch_news(stock_name)
    if not articles:
        return jsonify({"error": f"No news found for {stock_name}"}), 404

    analyzed_articles = analyze_news(articles)
    return jsonify(analyzed_articles)

@app.route("/get_technical_indicators")
def get_technical_indicators_route():
    stock = request.args.get("stock")
    data = aapl_data if stock == "AAPL" else reliance_data if stock == "RELIANCE.NS" else None
    if data is None:
        return jsonify({"error": "Invalid stock name"}), 400

    indicators = get_technical_indicators(data)
    return jsonify(indicators)

@app.route("/get_candlestick_chart")
def get_candlestick_chart_route():
    stock = request.args.get("stock")
    data = aapl_data if stock == "AAPL" else reliance_data if stock == "RELIANCE.NS" else None
    if data is None:
        return jsonify({"error": "Invalid stock name"}), 400

    img = get_candlestick_chart(data)
    return jsonify({"image": img})


@app.route("/predict_stock")
def predict_stock():
    stock = request.args.get("stock")
    duration = int(request.args.get("duration", 365))  # Default to 365 days
    amount = float(request.args.get("amount", 1000))  # Default to $1000
    data = aapl_data if stock == "AAPL" else reliance_data if stock == "RELIANCE.NS" else None
    
    if data is None:
        return jsonify({"error": "Invalid stock name"}), 400

    graph_html = predict_stock_price(stock, data, duration, amount)
    return jsonify({"graph": graph_html})

@app.route('/chatbot', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
