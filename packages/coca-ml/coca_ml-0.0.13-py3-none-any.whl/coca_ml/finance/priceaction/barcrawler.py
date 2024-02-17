from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from numba import njit

__all__ = ["BarCrawler"]


class BarCrawler(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame):
        i_cols = {name: i for i, name in enumerate(X.columns)}
        i_h = i_cols["high"]
        i_l = i_cols["low"]
        i_c = i_cols["close"]
        i_o = i_cols["open"]
        values = X.values
        sidebar = createSignal(values, i_h, i_l, i_c, i_o)
        X["sidebar"] = sidebar
        X[["sidebarU", "sidebarD"]] = 0
        X.loc[X.sidebar == 1, "sidebarU"] = 1
        X.loc[X.sidebar == -1, "sidebarD"] = 1
        return X.drop(columns=["sidebar"])


@njit
def sideBar(vals, mems, i_h, i_l, i_c, i_o):
    ret = 0
    if vals[i_c] > mems[0]:
        ret = 1
    elif vals[i_c] < mems[1]:
        ret = -1

    mems[0] = max(vals[i_h], mems[0]) if ret == 0 else vals[i_h]
    mems[1] = min(vals[i_l], mems[1]) if ret == 0 else vals[i_l]
    return ret


@njit
def createSignal(values, i_h, i_l, i_c, i_o):
    side_bar_mem = np.array([values[0, i_h], values[0, i_l]])
    side_bar = np.zeros(len(values))

    side_bar[0] = np.nan
    for i, val in enumerate(values[1:], 1):
        side_bar[i] = sideBar(val, side_bar_mem, i_h, i_l, i_c, i_o)
    return side_bar
