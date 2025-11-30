import numpy as np
import pandas as pd


class MLStrategy:
    """
    ML-based trading strategy.

    Supports:
        - Regression models (predict returns → convert to signals)
        - Classification models (predict +1 / 0 / -1 directly)
        - Probability thresholds for long/short entry
    """

    def __init__(
        self,
        model,
        feature_cols,
        prediction_type: str = "regression",
        long_threshold: float = 0.001,
        short_threshold: float = -0.001,
        allow_short: bool = True,
        prob_threshold: float = 0.55
    ):
        """
        Parameters:
            model: Pretrained ML model (sklearn, XGBoost, keras, PyTorch wrapper, etc.)
            feature_cols (list): Columns used as model inputs.
            prediction_type (str): "regression" or "classification".
            long_threshold (float): Min predicted return to go long.
            short_threshold (float): Max predicted return to go short.
            allow_short (bool): Enable short selling.
            prob_threshold (float): For classification probability cutoff.
        """
        self.model = model
        self.feature_cols = feature_cols
        self.prediction_type = prediction_type
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold
        self.allow_short = allow_short
        self.prob_threshold = prob_threshold

    # ---------------------------------------------------------
    # Generate ML-Based Signals
    # ---------------------------------------------------------
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """
        Uses ML model predictions to generate +1, 0, or -1 signals.
        """

        data = df.copy()

        # Ensure features exist
        missing_cols = [c for c in self.feature_cols if c not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing feature columns: {missing_cols}")

        X = data[self.feature_cols].values

        # ---------------------------------------------------------
        # 1) Regression Models (e.g., predict future % return)
        # ---------------------------------------------------------
        if self.prediction_type == "regression":

            preds = self.model.predict(X)

            signals = pd.Series(0, index=data.index)

            signals[preds > self.long_threshold] = +1

            if self.allow_short:
                signals[preds < self.short_threshold] = -1
            else:
                signals[preds < self.short_threshold] = 0

            return signals

        # ---------------------------------------------------------
        # 2) Classification Models
        # ---------------------------------------------------------
        elif self.prediction_type == "classification":

            # If model has predict_proba, use it
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X)
                # We assume class 1 = long, class 0 = short, modify as needed
                long_prob = probs[:, 1]

                signals = pd.Series(0, index=data.index)

                signals[long_prob > self.prob_threshold] = +1

                if self.allow_short:
                    signals[long_prob < (1 - self.prob_threshold)] = -1

                return signals

            # If no probabilities, assume raw class predictions
            else:
                preds = self.model.predict(X)

                # Expect +1, 0, -1 format; if not, convert automatically
                preds = pd.Series(preds, index=data.index)

                # Normalize predictions
                preds = preds.map(lambda x: +1 if x > 0 else (-1 if x < 0 else 0))

                if not self.allow_short:
                    preds[preds == -1] = 0

                return preds

        else:
            raise ValueError("prediction_type must be 'regression' or 'classification'")
