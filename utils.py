import numpy as np
import pandas as pd
from typing import Tuple


class Utils:
    """
    Utility functions for ML modeling, quant feature engineering,
    data processing, and experiment preparation.

    Includes:
        - Lag features
        - Rolling window features
        - Normalization
        - Train/test splitting
        - Feature validation
    """

    # ---------------------------------------------------------
    # FEATURE ENGINEERING
    # ---------------------------------------------------------
    @staticmethod
    def add_lag_features(df: pd.DataFrame, col: str, lags: int) -> pd.DataFrame:
        """
        Add lagged versions of a feature column (ideal for ML forecasting).
        Example: Price_{t-1}, Price_{t-2}, ...

        Parameters:
            df (pd.DataFrame)
            col (str): Column to generate lags for.
            lags (int): Number of lag features.

        Returns:
            pd.DataFrame: Includes new columns col_lag_1, col_lag_2, ...
        """
        df = df.copy()
        for i in range(1, lags + 1):
            df[f"{col}_lag_{i}"] = df[col].shift(i)
        return df

    @staticmethod
    def add_rolling_features(df: pd.DataFrame, col: str, windows: list) -> pd.DataFrame:
        """
        Generates rolling mean and std features.

        Parameters:
            df (pd.DataFrame)
            col (str): Column to generate rolling features.
            windows (list): List of window sizes.

        Returns:
            DataFrame with new features:
                col_roll_mean_{w}
                col_roll_std_{w}
        """
        df = df.copy()
        for w in windows:
            df[f"{col}_roll_mean_{w}"] = df[col].rolling(w).mean()
            df[f"{col}_roll_std_{w}"] = df[col].rolling(w).std()
        return df

    # ---------------------------------------------------------
    # NORMALIZATION
    # ---------------------------------------------------------
    @staticmethod
    def normalize_series(series: pd.Series) -> pd.Series:
        """Scale values to 0–1 using min-max normalization."""
        return (series - series.min()) / (series.max() - series.min() + 1e-9)

    @staticmethod
    def z_score(series: pd.Series) -> pd.Series:
        """Standard score normalization."""
        return (series - series.mean()) / (series.std() + 1e-9)

    # ---------------------------------------------------------
    # TRAIN/TEST SPLIT
    # ---------------------------------------------------------
    @staticmethod
    def time_series_split(
        df: pd.DataFrame,
        train_ratio: float = 0.8
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Chronological split for time series (no shuffling).

        Parameters:
            df (DataFrame)
            train_ratio (float): Proportion of data to use for training.

        Returns:
            train_df, test_df
        """
        split_idx = int(len(df) * train_ratio)
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        return train_df, test_df

    # ---------------------------------------------------------
    # FEATURE VALIDATION
    # ---------------------------------------------------------
    @staticmethod
    def validate_features(df: pd.DataFrame, required_cols: list):
        """
        Ensures all required feature columns exist.
        Raises ValueError if any are missing.
        """
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required feature columns: {missing}")

    # ---------------------------------------------------------
    # PREDICTION → SIGNAL HELPER
    # ---------------------------------------------------------
    @staticmethod
    def prediction_to_signals(preds, long_thresh=0.001, short_thresh=-0.001):
        """
        Convert numeric ML predictions into +1 / 0 / -1 signals.
        """
        preds = np.array(preds)
        signals = np.zeros_like(preds)

        signals[preds > long_thresh] = +1
        signals[preds < short_thresh] = -1

        return signals
