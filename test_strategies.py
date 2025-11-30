import pandas as pd
from src.strategies.sma_strategy import SMAStrategy
from src.strategies.rsi_strategy import RSIStrategy
from src.strategies.macd_strategy import MACDStrategy


def mock_price_df():
    return pd.DataFrame({
        "Close": [10, 11, 12, 11, 10, 9, 10, 11, 12, 13]
    })


def test_sma_strategy_generates_signals():
    df = mock_price_df()
    strat = SMAStrategy(short_window=2, long_window=4)
    signals = strat.generate_signals(df)
    assert isinstance(signals, pd.Series)
    assert set(signals.unique()).issubset({-1, 0, 1})


def test_rsi_strategy_generates_signals():
    df = mock_price_df()
    strat = RSIStrategy(window=3)
    signals = strat.generate_signals(df)
    assert isinstance(signals, pd.Series)
    assert set(signals.unique()).issubset({-1, 0, 1})


def test_macd_strategy_generates_signals():
    df = mock_price_df()
    strat = MACDStrategy()
    signals = strat.generate_signals(df)
    assert isinstance(signals, pd.Series)
