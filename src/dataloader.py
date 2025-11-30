import pandas as pd


class DataLoader:
    """
    Institutional-quality data ingestion module.
    Handles:
    - CSV ingestion
    - Date parsing
    - Sorting
    - Missing value cleaning
    - Validation for OHLCV data
    - Optional feature preprocessing hook
    """

    def __init__(
        self,
        filepath: str,
        date_col: str = "Date",
        parse_dates: bool = True,
        required_cols=None,
    ):
        """
        Parameters:
            filepath (str): Path to the CSV file.
            date_col (str): Column name representing dates.
            parse_dates (bool): Whether to parse date column.
            required_cols (list): Optional required columns (e.g., ["Close"]).
        """
        self.filepath = filepath
        self.date_col = date_col
        self.parse_dates = parse_dates
        self.required_cols = required_cols or ["Close"]

    # ---------------------------------------------------------
    # Load CSV File
    # ---------------------------------------------------------
    def load(self):
        """Load and return cleaned price data."""

        if self.parse_dates:
            df = pd.read_csv(self.filepath, parse_dates=[self.date_col])
        else:
            df = pd.read_csv(self.filepath)

        # Validate required columns
        for col in self.required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Ensure sorted by date
        if self.date_col in df.columns:
            df.sort_values(self.date_col, inplace=True)

        # Clean missing values
        df = df.dropna().reset_index(drop=True)

        return df

    # ---------------------------------------------------------
    # Load OHLCV (Optional)
    # ---------------------------------------------------------
    def load_ohlcv(self):
        """
        Load OHLCV datasets (Open, High, Low, Close, Volume).
        Common for quant strategies and ML forecasting.
        """

        ohlcv_cols = ["Open", "High", "Low", "Close", "Volume"]

        for col in ohlcv_cols:
            if col not in self.required_cols:
                self.required_cols.append(col)

        return self.load()

    # ---------------------------------------------------------
    # Feature Hook (Optional)
    # ---------------------------------------------------------
    def preprocess(self, df: pd.DataFrame):
        """
        Extend this to add custom features before backtesting.

        Example:
            df["Return"] = df["Close"].pct_change()
            df["LogReturn"] = np.log(df["Close"] / df["Close"].shift(1))
        """
        return df
