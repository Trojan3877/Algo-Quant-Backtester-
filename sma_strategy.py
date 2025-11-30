import pandas as pd
from ..indicators import sma


class SMAStrategy:
    """
    Simple Moving Average Crossover Strategy.

    Generates signals:
        +1 → Long
         0 → Flat
        -1 → Short (optional)
    
    Works with:
    - backtester.py
    - indicators.py
    """

    def __init__(self, window_fast=20, window_slow=50, allow_short=False):
        """
        Parameters:
            window_fast (int): Fast SMA window length.
            window_slow (int): Slow SMA window length.
            allow_short (bool): Enable short selling if True.
        """
        self.window_fast = window_fast
        self.window_slow = window_slow
        self.allow_short = allow_short

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Generate signal vector using SMA crossover logic.

        Returns:
            pd.Series: Signals (+1, 0, -1 depending on settings)
        """
        df = df.copy()

        df["SMA_Fast"] = sma(df["Close"], self.window_fast)
        df["SMA_Slow"] = sma(df["Close"], self.window_slow)

        df.dropna(inplace=True)

        # Long when fast SMA > slow SMA
        long_signal = df["SMA_Fast"] > df["SMA_Slow"]

        if self.allow_short:
            # Short when fast < slow
            signal = long_signal.astype(int) * 2 - 1   # +1 or -1
        else:
            # Only long or flat
            signal = long_signal.astype(int)

        signal = signal.reindex(df.index)

        return signal
