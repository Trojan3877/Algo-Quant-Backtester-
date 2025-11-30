import pandas as pd
import numpy as np
from .metrics import Metrics
from .plotting import Plotter


class Backtester:
    """
    Core backtesting engine for executing trading strategies.

    Designed for institutional-quality research:
    - Strategy plug-in system
    - Vectorized performance engine
    - Risk metrics (Sharpe, Sortino, MDD, etc.)
    - ML-compatible prediction + signal generation
    """

    def __init__(
        self,
        data_path: str,
        strategy,
        initial_capital: float = 100_000,
        commission: float = 0.0,
        slippage: float = 0.0,
    ):
        """
        Parameters:
            data_path (str): Path to CSV with market data (must contain 'Close').
            strategy (object): Strategy class instance with .generate_signals(data)
            initial_capital (float): Starting portfolio value.
            commission (float): Cost per trade.
            slippage (float): Price adjustment for fills.
        """
        self.data_path = data_path
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage

        self.data = None
        self.results = None

    # ---------------------------------------------------------
    # Load Data
    # ---------------------------------------------------------
    def load_data(self):
        """Load price data and validate."""
        df = pd.read_csv(self.data_path)

        required_cols = ["Close"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        df["Returns"] = df["Close"].pct_change()
        df.dropna(inplace=True)

        self.data = df

    # ---------------------------------------------------------
    # Execute Strategy
    # ---------------------------------------------------------
    def run(self):
        """Run the trading strategy and compute equity curve."""

        if self.data is None:
            self.load_data()

        # Strategy should return a vector of positions (+1, -1, 0)
        self.data["Signal"] = self.strategy.generate_signals(self.data)

        # Apply slippage
        close_price = self.data["Close"] * (1 + self.slippage)

        # PnL = position * next_day_return
        self.data["Strategy_Returns"] = (
            self.data["Signal"].shift(1) * self.data["Returns"]
        )
        self.data["Strategy_Returns"].fillna(0, inplace=True)

        # Transaction cost model
        self.data["Trade"] = self.data["Signal"].diff().abs()
        self.data["Transaction_Cost"] = self.data["Trade"] * self.commission

        self.data["Net_Returns"] = (
            self.data["Strategy_Returns"] - self.data["Transaction_Cost"]
        )

        # Equity Curve
        self.data["Equity"] = (
            self.initial_capital * (1 + self.data["Net_Returns"]).cumprod()
        )

        # Save results
        self.results = self.data

        return self.results

    # ---------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------
    def get_metrics(self):
        """Compute a full suite of professional quant metrics."""
        if self.results is None:
            raise RuntimeError("Run backtest before calling get_metrics().")

        m = Metrics(self.results["Net_Returns"], self.results["Equity"])
        return m.compute_all()

    # ---------------------------------------------------------
    # Plotting
    # ---------------------------------------------------------
    def plot(self):
        """Generate all standard backtesting plots."""
        if self.results is None:
            raise RuntimeError("Run backtest before calling plot().")

        p = Plotter(self.results)
        p.plot_equity_curve()
        p.plot_drawdown()
        p.plot_return_distribution()
        p.plot_rolling_sharpe()

    # ---------------------------------------------------------
    # Save Results
    # ---------------------------------------------------------
    def save_results(self, out_path="backtest_results.csv"):
        if self.results is None:
            raise RuntimeError("Run backtest before saving results.")
        self.results.to_csv(out_path, index=False)
