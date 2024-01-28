"""This module contains all methods to build the model and to make predictions."""

import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.var_model import VARResultsWrapper
from src.constants import YEARS


def fitVarModel(students: np.ndarray, salary: np.ndarray, graduates: np.ndarray, lags: int) -> VARResultsWrapper:
    """
    Fits a Vector Autoregression (VAR) model to the given data.

    Parameters:
    students (array-like): The number of students for each year.
    salary (array-like): The average salary for each year.
    graduates (array-like): The number of graduates for each year.
    lags (int): The maximum number of lags to use in the model.

    Returns:
    VARResultsWrapper: The results of the fitted VAR model.
    """
    dataset = np.column_stack((students, salary, graduates.repeat(2)))
    dataset = pd.DataFrame(dataset, index=YEARS[3:-4], columns=['students', 'salary', 'graduates'])
    model = VAR(dataset)
    results = model.fit(maxlags=lags)
    return results


def fitVarModelCompleteDataset(dataset: np.ndarray, lags: int) -> VARResultsWrapper:
    """
    Fits a Vector Autoregression (VAR) model to the given data.

    Parameters:
    dataset (array-like): The dataset to fit the model to.
    lags (int): The maximum number of lags to use in the model.

    Returns:
    VARResultsWrapper: The results of the fitted VAR model.
    """
    model = VAR(dataset)
    results = model.fit(maxlags=lags)
    return results


def predict(results: VARResultsWrapper, steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Makes a prediction using the fitted VAR model and also returns the standard error.

    Parameters:
    results (VARResultsWrapper): The results of the fitted VAR model.
    steps (int): The number of steps ahead to forecast.

    Returns:
    tuple: A tuple containing the forecasted values, the lower bound of the forecast interval, and the upper bound of the forecast interval.
    """
    forecast = results.forecast_interval(results.endog, steps=steps, alpha=0.05)
    return forecast


def predictWithData(results: VARResultsWrapper, data, steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Makes a prediction using the fitted VAR model and also returns the standard error.

    Parameters:
    results (VARResultsWrapper): The results of the fitted VAR model.
    steps (int): The number of steps ahead to forecast.

    Returns:
    tuple: A tuple containing the forecasted values, the lower bound of the forecast interval, and the upper bound of the forecast interval.
    """
    forecast = results.forecast_interval(data, steps=steps, alpha=0.05)
    return forecast
