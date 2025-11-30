import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sns.set_style("whitegrid")
sns.set_context("talk")


class Plotter:
    """
    A plotting utility that generates hedge-fund quality performance charts.

    Includes:
    - Equity Curve
    - Drawdown Curve
    - Return Distribution
    - Rolling Sharpe Ratio
    """

    def __init__(self, results: pd.DataFrame):
        if not isinstance(results, pd.DataFrame):
            raise TypeError("Plotter expects a pandas DataFrame.")

        required_cols = ["Equity", "Net_Returns"]
        for col in required_cols:
            if col not in results.columns:
                raise ValueError(f"Missing required column in results DataFrame: {col}")

        self.results = results

    # ---------------------------------------------------------
    # EQUITY CURVE
    # ---------------------------------------------------------
    def plot_equity_curve(self, save_path=None):
        plt.figure(figsize=(12, 6))
        plt.plot(self.results["Equity"], label="Equity Curve", color="#0066CC", linewidth=2)
        plt.title("Equity Curve", fontsize=18)
        plt.xlabel("Time")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        plt.show()

    # ---------------------------------------------------------
    # DRAWDOWN CURVE
    # ---------------------------------------------------------
    def plot_drawdown(self, save_path=None):
        rolling_max = self.results["Equity"].cummax()
        drawdown = (self.results["Equity"] - rolling_max) / rolling_max

        plt.figure(figsize=(12, 5))
        plt.plot(drawdown, color="#CC0000", linewidth=1.8)
        plt.title("Drawdown Curve", fontsize=18)
        plt.xlabel("Time")
        plt.ylabel("Drawdown")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        plt.show()

    # ---------------------------------------------------------
    # RETURN DISTRIBUTION
    # ---------------------------------------------------------
    def plot_return_distribution(self, save_path=None, bins=50):
        plt.figure(figsize=(10, 5))
        sns.histplot(self.results["Net_Returns"], bins=bins, kde=True, color="#009E73")
        plt.title("Return Distribution", fontsize=18)
        plt.xlabel("Net Returns")
        plt.ylabel("Frequency")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        plt.show()

    # ---------------------------------------------------------
    # ROLLING SHARPE RATIO
    # ---------------------------------------------------------
    def plot_rolling_sharpe(self, window=30, save_path=None):
        returns = self.results["Net_Returns"]
        rolling_sharpe = (
            returns.rolling(window).mean() / returns.rolling(window).std()
        ) * np.sqrt(252)

        plt.figure(figsize=(12, 5))
        plt.plot(rolling_sharpe, color="#8A2BE2", linewidth=2)
        plt.title(f"Rolling Sharpe Ratio ({window}-day window)", fontsize=18)
        plt.xlabel("Time")
        plt.ylabel("Sharpe Ratio")
        plt.axhline(0, color="black", linewidth=1)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        plt.show()
