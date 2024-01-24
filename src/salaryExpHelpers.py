import matplotlib.pyplot as plt
import numpy as np
from src.constants import COL_STUDENT, COL_STUDENT_PRED, COL_SALARY, COL_SALARY_PRED
from tueplots import bundles
import copy


def plot(data, forecast, years) -> plt.Figure:
    dataWithForecast = np.vstack((data, forecast))
    yearsWithForecast = np.append(years, [f"{i+1}" for i in range(forecast.shape[0])])

    plt.rcParams.update(bundles.icml2022(column="full", nrows=1, ncols=1, usetex=False))
    fig, ax1 = plt.subplots()
    plt.title('University Data Over the Years')
    plt.xticks(rotation=30)

    ax1.set_ylabel('Total students', color=COL_STUDENT)
    # Plot main data
    ax1.bar(yearsWithForecast[:-len(forecast)], dataWithForecast[:-len(forecast), 0], color=COL_STUDENT, label='Enrolled students')

    # Plot forecast with a different color
    ax1.bar(yearsWithForecast[-len(forecast):], dataWithForecast[-len(forecast):, 0],
            color=COL_STUDENT_PRED, label='Enrolled students forecast')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Sallary', color=COL_SALARY)

    # Plot main data
    ax2.plot(yearsWithForecast[:-len(forecast)], dataWithForecast[:-len(forecast), 1], color=COL_SALARY, label='Average brutto salary')

    # Plot forecast with a different color
    ax2.plot(yearsWithForecast[-len(forecast) - 1:], dataWithForecast[-len(forecast) - 1:, 1],
             color=COL_SALARY_PRED, label='Average brutto salary forecast')

    # Create one legend for both subplots
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    # Get current ticks, keep only every second tick
    locs, labels = plt.xticks()
    plt.xticks(locs[::2], labels[::2])


def modifySalary(data, func) -> np.ndarray:
    newData = copy.deepcopy(data)
    newData[:, 1] = np.array([func(d) for d in newData[:, 1]])
    return newData
