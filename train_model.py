#train_models.py
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import keras.backend as K
import tensorflow as tf

def train_model(stock, csv_file):
    # Load data
    data = pd.read_csv(csv_file, index_col="Date", parse_dates=True)
    
    # Preprocess
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data["Close"].values.reshape(-1, 1))

    # Create sequences
    seq_length = 60
    x_train, y_train = [], []
    for i in range(len(scaled_data) - seq_length - 1):
        x_train.append(scaled_data[i:i + seq_length])
        y_train.append(scaled_data[i + seq_length])
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Clear session
    K.clear_session()
    tf.keras.backend.clear_session()

    # Train Model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(x_train, y_train, epochs=20, batch_size=16, verbose=1)

    # Save model
    model.save(f"{stock}_lstm_model.h5")
    print(f"Model saved: {stock}_lstm_model.h5")

# Example Usage: python train_model.py RELIANCE.NS RELIANCE.NS_stock_data.csv
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python train_model.py <STOCK_NAME> <CSV_FILE>")
    else:
        train_model(sys.argv[1], sys.argv[2])
