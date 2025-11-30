import numpy as np
import pandas as pd


# ---------------------------------------------------------
# MOVING AVERAGES
# ---------------------------------------------------------

def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window).mean()


def ema(series: pd.Series, window: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=window, adjust=False).mean()


# ---------------------------------------------------------
# RSI
# ---------------------------------------------------------

def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index (RSI)."""
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# ---------------------------------------------------------
# MACD
# ---------------------------------------------------------

def macd(series: pd.Series, fast=12, slow=26, signal=9):
    """
    MACD = EMA(fast) - EMA(slow)
    Signal = EMA(MACD, signal)
    Histogram = MACD - Signal
    """
    ema_fast = ema(series, fast)
    ema_slow = ema(series, slow)

    macd_line = ema_fast - ema_slow
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


# ---------------------------------------------------------
# BOLLINGER BANDS
# ---------------------------------------------------------

def bollinger_bands(series: pd.Series, window=20, num_std=2):
    """
    Returns:
        middle_band, upper_band, lower_band
    """
    sma_val = sma(series, window)
    std = series.rolling(window).std()

    upper_band = sma_val + num_std * std
    lower_band = sma_val - num_std * std

    return sma_val, upper_band, lower_band


# ---------------------------------------------------------
# ATR - Average True Range
# ---------------------------------------------------------

def atr(df: pd.DataFrame, window=14):
    """
    Average True Range requires:
    High, Low, Close columns.
    """
    high_low = df["High"] - df["Low"]
    high_close = np.abs(df["High"] - df["Close"].shift())
    low_close = np.abs(df["Low"] - df["Close"].shift())

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(window).mean()


# ---------------------------------------------------------
# ROC - Rate of Change
# ---------------------------------------------------------

def roc(series: pd.Series, window=10):
    """Rate of Change."""
    return series.pct_change(periods=window)


# ---------------------------------------------------------
# STOCHASTIC OSCILLATOR
# ---------------------------------------------------------

def stochastic(df: pd.DataFrame, k_window=14, d_window=3):
    """
    Returns:
        %K, %D stochastic oscillator values
    """
    low_min = df["Low"].rolling(k_window).min()
    high_max = df["High"].rolling(k_window).max()

    percent_k = 100 * (df["Close"] - low_min) / (high_max - low_min)
    percent_d = percent_k.rolling(d_window).mean()

    return percent_k, percent_d
