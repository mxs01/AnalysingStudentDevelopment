import matplotlib.pyplot as plt

import copy
import os

from typing import List, Callable

import numpy as np
from src.constants import COL_STUDENT, COL_STUDENT_PRED, COL_SALARY, COL_SALARY_PRED, FIG_DIR
from tueplots import bundles


def plot(data: np.ndarray, forecast: np.ndarray, ogForecast: np.ndarray, years: List[str], name: str, lags: int) -> plt.Figure:
        """ creates plot, that visualizes the influence of the manipulated data

        Args:
            data (: np.ndarray): the completeData used for training the model
            forecast (: np.ndarray): prediction from model with given data
            ogForecast (: np.ndarray): original prediction, without data manipulation
            years (List[str]): list of specified years
            name (str): filename for saving
            lags (int): the lags we consider

        Returns:
            plt.Figure: creates matplotlib plot that shows difference between 
        """
        dataWithForecast = np.vstack((data, forecast))
        ogDataWithForecast = np.vstack((data, ogForecast))
        yearsWithForecast = np.append(years, [f"{i+1}" for i in range(forecast.shape[0])])

        plt.rcParams.update(bundles.icml2022(column="half", nrows=1, ncols=1, usetex=False))
        fig, ax1 = plt.subplots()
        plt.title('Enrolled students with altered salary')
        plt.xticks(rotation=30)

        ax1.set_ylim([0, 10000])
        ax1.set_ylabel('Total students', color=COL_STUDENT)
        # Plot main data
        ax1.bar(yearsWithForecast[:-len(forecast)], dataWithForecast[:-len(forecast), 0], color=COL_STUDENT, label='Enrolled students')

        # Plot forecast with a different color
        ax1.bar(yearsWithForecast[-len(forecast):], dataWithForecast[-len(forecast):, 0],
                color=COL_STUDENT_PRED, label='Enrolled students forecast')

        # Plot original forecast with a different color
        ax1.bar(yearsWithForecast[-len(forecast):], ogDataWithForecast[-len(forecast):, 0],
                color='silver', label='Original prediction', alpha=0.5)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('Salary', color=COL_SALARY)

        # Plot main data
        ax2.plot(yearsWithForecast[:-len(forecast)], dataWithForecast[:-len(forecast), 1], color=COL_SALARY, label='Average gross salary')

        # Plot forecast with a different color
        ax2.plot(yearsWithForecast[-len(forecast) - 1:], dataWithForecast[-len(forecast) - 1:, 1],
                color=COL_SALARY_PRED, label='Average gross salary  forecast')

        # Create one legend for both subplots
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        # Get current ticks, keep only every second tick
        locs, labels = plt.xticks()
        plt.xticks(locs[::2], labels[::2])
        fig.savefig(os.path.join(FIG_DIR, f"{name}_{lags}.pdf"))


def modifySalary(data: np.ndarray, func: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
        """ modifies time series with a higher order function

        Args:
            data (np.ndarray): salary data
            func (Callable[[np.ndarray],np.ndarray]): function, which manipulates salary data

        Returns:
            np.ndarray: manipulated salary data
        """
        newData = copy.deepcopy(data)
        newData[:, 1] = np.array([func(d) for d in newData[:, 1]])
        return newData
