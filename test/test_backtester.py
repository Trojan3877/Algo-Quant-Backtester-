import pandas as pd
from src.backtester import Backtester
from src.strategies.sma_strategy import SMAStrategy


def test_backtester_runs():
    df = pd.DataFrame({"Close": [10, 11, 12, 11, 10, 9, 8, 9]})
    strat = SMAStrategy(short_window=2, long_window=3)

    bt = Backtester(df=df, strategy=strat)
    results = bt.run()

    assert "returns" in results.columns
    assert "equity_curve" in results.columns
    assert len(results) > 0


def test_backtester_handles_signals():
    df = pd.DataFrame({"Close": [10, 9, 11, 12, 10]})
    strat = SMAStrategy(short_window=1, long_window=2)

    bt = Backtester(df=df, strategy=strat)
    results = bt.run()

    assert not results["signal"].isna().all()
