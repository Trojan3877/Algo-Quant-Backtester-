"""
build_features.py

Module: Feature Engineering
Author: Corey Leath

Reads raw market data, computes technical indicators and features,
and writes the processed dataset for model training.
"""

import pandas as pd
import ta  # Technical Analysis library

def main():
    # Load raw historical data
    df = pd.read_parquet("data/raw/spy.parquet", engine="pyarrow")
    
    # Ensure timestamp is datetime and sorted
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    
    # Compute technical indicators
    df["sma_20"] = ta.trend.sma_indicator(df["close"], window=20)
    df["rsi_14"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    df["atr_14"] = ta.volatility.AverageTrueRange(
        df["high"], df["low"], df["close"], window=14
    ).average_true_range()
    
    # Drop rows with NaNs
    df.dropna(inplace=True)
    
    # Save features
    df.to_csv("data/processed/features.csv", index=False)
    print(f"[Features] Generated {len(df)} rows with features.")

if __name__ == "__main__":
    main()

git add src/features/build_features.py
git commit -m "Add feature engineering module"
git push
