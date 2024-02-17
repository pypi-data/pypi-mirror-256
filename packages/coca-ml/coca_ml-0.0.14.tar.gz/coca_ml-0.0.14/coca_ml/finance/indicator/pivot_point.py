from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from datetime import timedelta

__all__ = ["PivotPoint"]


class PivotPoint(BaseEstimator, TransformerMixin):
    _resample_tbl = {
        timedelta(minutes=1): "d",
        timedelta(minutes=5): "d",
        timedelta(minutes=10): "d",
        timedelta(minutes=15): "d",
        timedelta(minutes=30): "w",
        timedelta(hours=1): "w",
        timedelta(hours=2): "w",
        timedelta(days=1): "MS",
        timedelta(days=7): "YS",
    }
    _agg_procs: dict = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
    }

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame):
        resample = X.resample(self._resample_tbl[X.index[1] - X.index[0]]).agg(
            self._agg_procs
        )

        resample["pivot_point"] = (
            resample.high + resample.low + resample.close
        ) / 3

        resample = self._standard(resample)
        resample = self._fibonacci(resample)
        resample = self._demark(resample)
        resample = resample.drop(
            columns=["open", "high", "low", "close"]
        ).shift(1)
        return X.merge(
            resample, how="left", left_index=True, right_index=True
        ).ffill()

    def _standard(self, X):
        X["standard_S1"] = (X.pivot_point * 2) - X.high
        X["standard_S2"] = X.pivot_point - (X.high - X.low)
        X["standard_R1"] = (X.pivot_point * 2) - X.low
        X["standard_R2"] = X.pivot_point + (X.high - X.low)
        return X

    def _fibonacci(self, X):
        X["fibonacci_S1"] = X.pivot_point - (0.382 * (X.high - X.low))
        X["fibonacci_S2"] = X.pivot_point - (0.618 * (X.high - X.low))
        X["fibonacci_S3"] = X.pivot_point - (1 * (X.high - X.low))
        X["fibonacci_R1"] = X.pivot_point + (0.382 * (X.high - X.low))
        X["fibonacci_R2"] = X.pivot_point + (0.618 * (X.high - X.low))
        X["fibonacci_R3"] = X.pivot_point + (1 * (X.high - X.low))
        return X

    def _demark(self, X):
        X.loc[X.close < X.open, "x"] = X.high + (2 * X.low) + X.close
        X.loc[X.close > X.open, "x"] = (2 * X.high) + X.low + X.close
        X.loc[X.close == X.open, "x"] = X.high + X.low + (2 * X.close)
        X["demark_pivot_point"] = X.x / 4
        X["demark_S1"] = X.x / 2 - X.high
        X["demark_R1"] = X.x / 2 - X.low
        return X.drop(columns=["x"])
