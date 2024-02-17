from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

__all__ = ["ThrustUD"]


class ThrustUD(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame):
        cols = [("prelow", "low"), ("prehigh", "high")]
        newcol = ["thrustU", "thrustD"]

        for precol, nowcol in cols:
            X[precol] = X[nowcol].shift(1)

        X[newcol] = 0
        X.loc[X.prehigh < X.close, newcol[0]] = 1
        X.loc[X.prelow > X.close, newcol[1]] = 1
        X.loc[X.index[0], newcol] = np.nan
        return X.drop(columns=[pre for pre, _ in cols])
