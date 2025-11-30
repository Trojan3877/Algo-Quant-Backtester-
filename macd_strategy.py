import pandas as pd
from ..indicators import macd


class MACDStrategy:
    """
    MACD (Moving Average Convergence Divergence) Strategy.

    Signal Logic:
        - MACD line crosses ABOVE signal line → Buy (+1)
        - MACD line crosses BELOW signal line → Sell (-1 or 0)
    """

    def __init__(
        self,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
        allow_short: bool = False
    ):
        """
        Parameters:
            fast (int): Fast EMA period.
            slow (int): Slow EMA period.
            signal (int): Signal line EMA period.
            allow_short (bool): Enable short signals.
        """
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.allow_short = allow_short

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals using MACD crossovers.

        Returns:
            pd.Series: Vector of +1, 0, or -1.
        """
        df = df.copy()
        df["MACD"], df["Signal"], df["Hist"] = macd(
            df["Close"],
            fast=self.fast,
            slow=self.slow,
            signal=self.signal
        )

        df.dropna(inplace=True)

        signals = pd.Series(0, index=df.index)

        # Crossover signals
        crossover_up = df["MACD"] > df["Signal"]
        crossover_down = df["MACD"] < df["Signal"]

        # Long on bullish crossover
        signals[crossover_up] = +1

        if self.allow_short:
            signals[crossover_down] = -1
        else:
            signals[crossover_down] = 0

        return signals
