# stock_analysis.py
import pandas as pd
import plotly.graph_objects as go
import re

def get_technical_indicators(data):
    data = data.copy()
    
    # Simple Moving Average (SMA) & Bollinger Bands
    data["SMA"] = data["Close"].rolling(window=20).mean()
    data["Upper_BB"] = data["SMA"] + (data["Close"].rolling(window=20).std() * 2)
    data["Lower_BB"] = data["SMA"] - (data["Close"].rolling(window=20).std() * 2)
    
    # Relative Strength Index (RSI)
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))
    
    # Moving Average Convergence Divergence (MACD)
    data["EMA12"] = data["Close"].ewm(span=12, adjust=False).mean()
    data["EMA26"] = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = data["EMA12"] - data["EMA26"]
    data["Signal_Line"] = data["MACD"].ewm(span=9, adjust=False).mean()
    
    # Volume Analysis
    data["Volume_MA"] = data["Volume"].rolling(window=20).mean()

    # Price Chart (SMA & Bollinger Bands)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close Price", line=dict(color="blue")))
    fig1.add_trace(go.Scatter(x=data.index, y=data["SMA"], mode="lines", name="SMA (20-day)", line=dict(color="orange", dash="dash")))
    fig1.add_trace(go.Scatter(x=data.index, y=data["Upper_BB"], mode="lines", name="Upper BB", line=dict(color="gray"), opacity=0.5))
    fig1.add_trace(go.Scatter(x=data.index, y=data["Lower_BB"], mode="lines", name="Lower BB", line=dict(color="gray"), opacity=0.5))
    fig1.update_layout(title="Stock Price with SMA & Bollinger Bands", xaxis_title="Date", yaxis_title="Price", xaxis_rangeslider_visible=False)

    # RSI Chart
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI", line=dict(color="purple")))
    fig2.add_hline(y=70, line=dict(color="red", dash="dash"), annotation_text="Overbought", annotation_position="top right")
    fig2.add_hline(y=30, line=dict(color="green", dash="dash"), annotation_text="Oversold", annotation_position="bottom right")
    fig2.update_layout(title="Relative Strength Index (RSI)", xaxis_title="Date", yaxis_title="RSI", xaxis_rangeslider_visible=False)

    # MACD Chart
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=data.index, y=data["MACD"], mode="lines", name="MACD", line=dict(color="blue")))
    fig3.add_trace(go.Scatter(x=data.index, y=data["Signal_Line"], mode="lines", name="Signal Line", line=dict(color="red", dash="dash")))
    fig3.update_layout(title="Moving Average Convergence Divergence (MACD)", xaxis_title="Date", yaxis_title="MACD", xaxis_rangeslider_visible=False)

    # Volume Analysis Chart
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=data.index, y=data["Volume"], name="Volume", marker=dict(color="blue", opacity=0.5)))
    fig4.add_trace(go.Scatter(x=data.index, y=data["Volume_MA"], mode="lines", name="20-day Volume MA", line=dict(color="red", dash="dash")))
    fig4.update_layout(title="Volume Analysis", xaxis_title="Date", yaxis_title="Volume", xaxis_rangeslider_visible=False)

    # Convert to HTML and clean unwanted metadata
    clean_html1 = re.sub(r'window.PlotlyConfig.*?;', '', fig1.to_html(full_html=False), flags=re.DOTALL)
    clean_html2 = re.sub(r'window.PlotlyConfig.*?;', '', fig2.to_html(full_html=False), flags=re.DOTALL)
    clean_html3 = re.sub(r'window.PlotlyConfig.*?;', '', fig3.to_html(full_html=False), flags=re.DOTALL)
    clean_html4 = re.sub(r'window.PlotlyConfig.*?;', '', fig4.to_html(full_html=False), flags=re.DOTALL)

    return {"price_chart": clean_html1, "rsi_chart": clean_html2, "macd_chart": clean_html3, "volume_chart": clean_html4}

def get_candlestick_chart(data):
    """Generates an interactive candlestick chart for stock data."""
    data = data.copy()
    
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    fig.update_layout(title="Candlestick Chart", xaxis_rangeslider_visible=False)

    # Get raw HTML and clean it
    raw_html = fig.to_html(full_html=False)
    clean_html = re.sub(r'window.PlotlyConfig.*?;', '', raw_html, flags=re.DOTALL)

    return clean_html
