import numpy as np
import pandas as pd


class Metrics:
    """
    Professional-grade quantitative performance metrics engine.
    Compatible with:
    - Quant hedge fund standards (Two Sigma / Citadel / HRT)
    - ML-based trading evaluation
    """

    def __init__(self, returns: pd.Series, equity: pd.Series, trading_days: int = 252):
        """
        Parameters:
            returns (pd.Series): Net strategy returns per bar (after costs).
            equity (pd.Series): Equity curve.
            trading_days (int): Annualization factor (default 252 for daily bars).
        """
        self.returns = returns
        self.equity = equity
        self.trading_days = trading_days

    # ---------------------------------------------------------
    # Core Metrics
    # ---------------------------------------------------------
    def cagr(self):
        """Compound Annual Growth Rate."""
        total_return = self.equity.iloc[-1] / self.equity.iloc[0]
        years = len(self.equity) / self.trading_days
        return total_return ** (1 / years) - 1 if total_return > 0 else -1.0

    def volatility(self):
        """Annualized volatility."""
        return np.std(self.returns) * np.sqrt(self.trading_days)

    def sharpe(self, risk_free_rate: float = 0.0):
        """Sharpe Ratio."""
        excess_returns = self.returns - (risk_free_rate / self.trading_days)
        vol = self.volatility()
        return np.sqrt(self.trading_days) * excess_returns.mean() / vol if vol > 0 else 0.0

    def sortino(self, risk_free_rate: float = 0.0):
        """Sortino Ratio (downside-risk adjusted)."""
        excess_returns = self.returns - (risk_free_rate / self.trading_days)
        downside = np.std(excess_returns[excess_returns < 0])
        return (
            np.sqrt(self.trading_days) * excess_returns.mean() / downside
            if downside > 0
            else 0.0
        )

    def max_drawdown(self):
        """Maximum Drawdown (MDD)."""
        roll_max = self.equity.cummax()
        dd = (self.equity - roll_max) / roll_max
        return dd.min()

    def calmar(self):
        """Calmar Ratio (CAGR / Max Drawdown)."""
        mdd = abs(self.max_drawdown())
        return self.cagr() / mdd if mdd > 0 else 0.0

    # ---------------------------------------------------------
    # Trade statistics
    # ---------------------------------------------------------
    def win_rate(self):
        wins = (self.returns > 0).sum()
        losses = (self.returns < 0).sum()
        return wins / (wins + losses) if (wins + losses) > 0 else 0.0

    def profit_factor(self):
        """Gross profit / Gross loss."""
        gross_profit = self.returns[self.returns > 0].sum()
        gross_loss = abs(self.returns[self.returns < 0].sum())
        return gross_profit / gross_loss if gross_loss > 0 else np.inf

    def expectancy(self):
        """
        Average return per trade.
        Expectancy > 0 is generally profitable.
        """
        return self.returns.mean()

    def average_win(self):
        wins = self.returns[self.returns > 0]
        return wins.mean() if len(wins) > 0 else 0.0

    def average_loss(self):
        losses = self.returns[self.returns < 0]
        return losses.mean() if len(losses) > 0 else 0.0

    def payoff_ratio(self):
        """Average win magnitude / Average loss magnitude."""
        avg_win = self.average_win()
        avg_loss = abs(self.average_loss())
        return avg_win / avg_loss if avg_loss > 0 else np.inf

    # ---------------------------------------------------------
    # Rolling Metrics
    # ---------------------------------------------------------
    def rolling_sharpe(self, window: int = 30):
        """Rolling Sharpe Ratio (for plotting)."""
        return (
            self.returns.rolling(window).mean()
            / self.returns.rolling(window).std()
        ) * np.sqrt(self.trading_days)

    # ---------------------------------------------------------
    # Output Dictionary
    # ---------------------------------------------------------
    def compute_all(self):
        """Return all metrics in a dictionary (for MLFlow, logging, printing)."""

        return {
            "CAGR": round(self.cagr(), 6),
            "Volatility": round(self.volatility(), 6),
            "Sharpe Ratio": round(self.sharpe(), 6),
            "Sortino Ratio": round(self.sortino(), 6),
            "Max Drawdown": round(self.max_drawdown(), 6),
            "Calmar Ratio": round(self.calmar(), 6),
            "Win Rate": round(self.win_rate(), 6),
            "Profit Factor": round(self.profit_factor(), 6),
            "Expectancy": round(self.expectancy(), 6),
            "Average Win": round(self.average_win(), 6),
            "Average Loss": round(self.average_loss(), 6),
            "Payoff Ratio": round(self.payoff_ratio(), 6),
        }
