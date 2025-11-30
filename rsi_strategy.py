import pandas as pd
from ..indicators import rsi


class RSIStrategy:
    """
    RSI Overbought/Oversold Mean-Reversion or Trend Strategy.

    Signal Logic:
        - If RSI < oversold → Buy (+1)
        - If RSI > overbought → Sell (-1 or 0 depending on `allow_short`)
        - Otherwise → Hold (previous position)
    """

    def __init__(
        self,
        window: int = 14,
        overbought: float = 70,
        oversold: float = 30,
        allow_short: bool = False,
    ):
        """
        Parameters:
            window (int): RSI window length.
            overbought (float): Overbought threshold.
            oversold (float): Oversold threshold.
            allow_short (bool): Enable short selling if True.
        """
        self.window = window
        self.overbought = overbought
        self.oversold = oversold
        self.allow_short = allow_short

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals using RSI threshold rules.

        Returns:
            pd.Series: Signals vector (+1, 0, or -1)
        """
        df = df.copy()
        df["RSI"] = rsi(df["Close"], window=self.window)

        df.dropna(inplace=True)

        signals = pd.Series(0, index=df.index)

        # Oversold → Buy
        signals[df["RSI"] < self.oversold] = +1

        if self.allow_short:
            # Overbought → Short
            signals[df["RSI"] > self.overbought] = -1
        else:
            # Overbought → Go flat
            signals[df["RSI"] > self.overbought] = 0

        return signals
