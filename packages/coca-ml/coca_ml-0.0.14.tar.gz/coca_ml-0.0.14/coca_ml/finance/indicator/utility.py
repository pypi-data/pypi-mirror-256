# %%
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

__all__ = ["Utility"]


class Utility(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame):
        X = self._ultimateOscillator(X)
        return X

    def _ultimateOscillator(self, X: pd.DataFrame):
        X["preclose"] = X.close.shift(1)
        X["BP"] = X.close[1:] - X.loc[X.index[1:], ["low", "preclose"]].min(
            axis=1
        )

        X["TR"] = X.loc[X.index[1:], ["high", "preclose"]].max(axis=1) - X.loc[
            X.index[1:], ["low", "preclose"]
        ].min(axis=1)
        return X.drop(columns="preclose")


df = pd.read_pickle("dataCrypt.pkl")
Utility().fit_transform(df)
