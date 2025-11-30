import pandas as pd
from src.utils import Utils


def test_lag_features():
    df = pd.DataFrame({"Close": [1, 2, 3, 4]})
    df2 = Utils.add_lag_features(df, "Close", lags=2)
    assert "Close_lag_1" in df2.columns
    assert df2["Close_lag_1"].iloc[1] == 1


def test_rolling_features():
    df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]})
    df2 = Utils.add_rolling_features(df, "Close", windows=[3])
    assert "Close_roll_mean_3" in df2.columns
    assert df2["Close_roll_mean_3"].iloc[2] == 2.0


def test_normalization():
    s = pd.Series([10, 20, 30])
    n = Utils.normalize_series(s)
    assert round(n.iloc[-1], 2) == 1.00


def test_time_series_split():
    df = pd.DataFrame({"Close": range(10)})
    train, test = Utils.time_series_split(df, 0.7)
    assert len(train) == 7
    assert len(test) == 3
