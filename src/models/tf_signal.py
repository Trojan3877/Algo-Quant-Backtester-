"""
tf_signal.py

Module: TensorFlow Signal Model
Author: Corey Leath

Defines and trains an LSTM model in TensorFlow/Keras to predict next-period returns.
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import os

def build_model(input_shape):
    """
    Build and compile the LSTM model.
    
    Args:
        input_shape (tuple): Shape of the input data (timesteps, features).
        
    Returns:
        tf.keras.Model: Compiled LSTM model.
    """
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(64, input_shape=input_shape),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def load_data(window_size=10):
    """
    Load processed features and prepare sequences for LSTM.
    
    Args:
        window_size (int): Number of past timesteps to use as input.
    
    Returns:
        X (np.ndarray), y (np.ndarray)
    """
    df = pd.read_csv("data/processed/features.csv", parse_dates=['timestamp'])
    values = df[['close', 'sma_20', 'rsi_14', 'atr_14']].values
    X, y = [], []
    for i in range(len(values) - window_size):
        X.append(values[i:i+window_size])
        y.append(values[i+window_size][0] - values[i+window_size-1][0])  # predict return
    return np.array(X), np.array(y)

def main():
    window_size = int(os.getenv("WINDOW_SIZE", 10))
    X, y = load_data(window_size=window_size)
    # Split
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Build and train
    model = build_model(input_shape=X_train.shape[1:])
    model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.1)
    
    # Evaluate
    loss, mae = model.evaluate(X_test, y_test)
    print(f"[TF Model] Test MAE: {mae:.4f}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    model.save("models/tf_signal.h5")
    print("[TF Model] Saved TensorFlow model to models/tf_signal.h5")

if __name__ == "__main__":
    main()

git add src/models/tf_signal.py
git commit -m "Add TensorFlow LSTM signal model module"
git push
