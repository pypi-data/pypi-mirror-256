from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

__all__ = ["ReversalHL"]


class ReversalHL(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame):
        cols = [
            ("prehigh", "high"),
            ("prelow", "low"),
            ("preclose", "close"),
            ("preopen", "open"),
        ]
        dropcol = [pre for pre, _ in cols] + ["presign"]
        newcol = ["reversalH", "reversalSH", "reversalL", "reversalSL"]

        for pre, now in cols:
            X[pre] = X[now].shift(1)
        X[dropcol[-1]] = X.preclose - X.preopen

        X[newcol] = 0
        X.loc[
            (X.presign > 0) & (X.prehigh < X.high) & (X.preopen > X.close),
            newcol[0],
        ] = 1
        X.loc[
            (X.presign > 0) & (X.prehigh < X.high) & (X.prelow > X.close),
            newcol[1],
        ] = 1

        X.loc[
            (X.presign < 0) & (X.prelow > X.low) & (X.preopen < X.close),
            newcol[2],
        ] = 1
        X.loc[
            (X.presign < 0) & (X.prelow > X.low) & (X.prehigh < X.close),
            newcol[3],
        ] = 1
        X.loc[X.index[0], newcol] = np.nan
        return X.drop(columns=dropcol)
