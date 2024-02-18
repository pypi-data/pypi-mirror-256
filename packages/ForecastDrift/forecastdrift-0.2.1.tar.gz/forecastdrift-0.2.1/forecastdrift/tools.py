import numpy as np
import pandas as pd
def rows_counter(y_true, y_pred):
    """
    Count the number of rows that have valid forecasts in a Data Frame, np.Arr.
    :param y_true: Used only for sklearn compatibility
    :param y_pred: Predicted values
    :return: A simple count of predicted (non-NA values)
    """

    if isinstance(y_pred, np.ndarray):
        y_pred = pd.Series(y_pred)
    return y_pred.dropna().shape[0]