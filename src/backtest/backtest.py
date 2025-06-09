"""
backtest.py

Module: Backtesting Engine
Author: Corey Leath

Performs backtests for both TensorFlow and PyTorch models over processed features,
using walk-forward analysis and recording performance metrics.
"""

import pandas as pd
import numpy as np
import joblib
import torch
from src.models.tf_signal import build_model
from src.models.torch_rl import DQNAgent
import yaml
import os

def load_features(path="data/processed/features.csv"):
    """Load engineered features into DataFrame."""
    df = pd.read_csv(path, parse_dates=['timestamp'])
    return df

def walk_forward_backtest(df, model_type, config):
    """
    Perform walk-forward backtest.
    
    Args:
        df (pd.DataFrame): Features with timestamp.
        model_type (str): 'tf' or 'torch'.
        config (dict): Backtest settings.
    
    Returns:
        results (pd.DataFrame): Backtest PnL or returns over time.
    """
    window = config['window']
    step = config['step']
    results = []
    
    for start in range(0, len(df) - window, step):
        train_df = df.iloc[start:start + window]
        test_df = df.iloc[start + window:start + window + config['horizon']]
        
        # Load and predict
        if model_type == 'tf':
            model = tf.keras.models.load_model("models/tf_signal.h5")
            X_test = train_df[['sma_20', 'rsi_14', 'atr_14']].tail(config['horizon']).values.reshape(-1, config['horizon'], 3)
            preds = model.predict(X_test).flatten()
        else:
            agent = DQNAgent(state_dim=1, action_dim=3)
            agent.load_state_dict(torch.load("models/torch_rl_agent.pth"))
            agent.eval()
            # Simplified: use closing return as state
            states = test_df['close'].pct_change().dropna().values.reshape(-1, 1)
            with torch.no_grad():
                preds = agent(torch.tensor(states, dtype=torch.float32)).argmax(dim=1).numpy()
        
        # Compute PnL or return metric
        actual_returns = test_df['close'].pct_change().fillna(0).values
        pnl = np.sum(preds * actual_returns)  # simplistic PnL
        results.append({
            'start': df.iloc[start]['timestamp'],
            'end': test_df.iloc[-1]['timestamp'],
            'pnl': pnl
        })
    
    return pd.DataFrame(results)

def main(config_path="configs/backtest.yaml"):
    """Load config, run backtest for each model, and save results."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    df = load_features()
    
    # Run for TF model
    tf_results = walk_forward_backtest(df, 'tf', config)
    tf_results.to_csv("backtest/tf_backtest.csv", index=False)
    
    # Run for Torch RL model
    torch_results = walk_forward_backtest(df, 'torch', config)
    torch_results.to_csv("backtest/torch_backtest.csv", index=False)
    
    print("Backtests completed. Results saved to backtest/*.csv")

if __name__ == "__main__":
    # Ensure backtest directory exists
    os.makedirs("backtest", exist_ok=True)
    main()

git add src/backtest/backtest.py
git commit -m "Add backtesting engine with walk-forward analysis"
git push
