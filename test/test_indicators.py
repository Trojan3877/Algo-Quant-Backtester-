import pandas as pd
from src.indicators import sma, ema, rsi, macd


def test_sma():
    s = pd.Series([1, 2, 3, 4, 5])
    result = sma(s, 3)
    assert round(result.iloc[-1], 2) == 4.00


def test_ema():
    s = pd.Series([1, 2, 3, 4, 5])
    result = ema(s, 3)
    assert result.iloc[-1] > 3.0  # EMA always closer to recent


def test_rsi():
    s = pd.Series([1, 2, 3, 2, 1, 2, 3])
    result = rsi(s, 3)
    assert result.dropna().between(0, 100).all()


def test_macd():
    s = pd.Series([1, 2, 3, 4, 5, 6, 7])
    dif, signal, hist = macd(s)
    assert len(dif) == len(signal) == len(hist)
