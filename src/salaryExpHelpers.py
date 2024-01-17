import matplotlib.pyplot as plt
import numpy as np


def plot(data, forecast, years) -> plt.Figure:
    dataWithForecast = np.vstack((data, forecast))
    yearsWithForecast = np.append(years, [f"{i+1}" for i in range(forecast.shape[0])])

    fig, ax1 = plt.subplots()
    plt.title('University Data Over the Years')
    plt.xticks(rotation='vertical')
    plt.axvspan(len(data), len(dataWithForecast) - 1, alpha=0.5, color='lightgrey')

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total students and Graduates in BW', color='tab:blue')
    ax1.bar(yearsWithForecast, dataWithForecast[:, 0], color='tab:blue', label='Total students')  # Changed to bar
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Average brutto sallary', color=color)  # we already handled the x-label with ax1
    ax2.plot(yearsWithForecast, dataWithForecast[:, 1], color=color, label='Average brutto sallary')
    ax2.tick_params(axis='y', labelcolor=color)

    # Create one legend for both subplots
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')


def modifySalary(data, func) -> np.ndarray:
    data[:, 1] = np.array([func(d) for d in data[:, 1]])
    return data
