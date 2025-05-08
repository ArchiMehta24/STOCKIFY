#Run this file before running run_app.sh

import pandas as pd
import yfinance as yf
import datetime as dt
import os

def fetch_and_store_stock_data():
    # User Inputs
    ticker = input("Enter Stock Ticker Symbol (e.g., AAPL, MSFT): ").strip().upper()
    from_date = input("Enter start date (YYYY-MM-DD): ").strip()
    to_date = input("Enter end date (YYYY-MM-DD): ").strip()

    # Convert input strings to datetime
    try:
        start = dt.datetime.strptime(from_date, "%Y-%m-%d")
        end = dt.datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Please enter dates in YYYY-MM-DD format.")
        return None

    # File path (auto-saves in Google Colab session)
    file_path = f"/content/{ticker}_stock_data.csv"

    # Check if the CSV file already exists
    if os.path.exists(file_path):
        print(f"📂 Data already exists in {file_path}. No need to fetch again.")
    else:
        print(f"⏳ Fetching new stock data for {ticker} from Yahoo Finance...")
        try:
            data = yf.download(ticker, start=start, end=end)
            if data.empty:
                print("❌ No stock data found for the given date range.")
                return None
            data.to_csv(file_path)  # Save data in Colab
            print(f"✅ Stock data saved at: {file_path}")
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None

    return ticker  # Return the ticker symbol

# Run this block once
ticker_symbol = fetch_and_store_stock_data()