import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

import os


def GetGraduatesData():

    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_DIR, "dat")
    GRADUATES_PATH = os.path.join(DATA_DIR, "graduates_germany.csv")

    """
    SALLARY_PATH = os.path.join(DATA_DIR, "sallary_per_sector.csv")
    GENDER_DATA_PATH = os.path.join(DATA_DIR, "university_gender_divided_stem.xlsx")
    STUDENTS_PATH = os.path.join(DATA_DIR, "student_data_per_subject.xlsx")
    PLOT_DIR = os.path.join(PROJECT_DIR, 'plots')
    """

    # file_path = '/Users/abdallahabdul-latif/Desktop/Universität Tübingen/5.Semester/Data Literacy/StudentProject/AnalysingStudentDevelopment/data/graduates_germany.csv'
    file_path = GRADUATES_PATH
    data = pd.read_csv(file_path, encoding="ISO-8859-1", sep=";", decimal=".", skiprows=4, skipfooter=3, engine="python")

    # Now manually assign the first column as 'year' and the second as 'gender'
    data.columns = ['gender', 'year'] + ['state_' + str(i) for i in range(1, len(data.columns) - 1)]

    # Convert the 'year' to string for consistency
    data['year'] = data['year'].astype(str)

    # Filter out rows that do not contain the desired year format (e.g., '2006/07')
    data_with_years = data[data['year'].str.contains(r'20\d{2}/\d{2}', regex=True)]

    # Define the range of years we are interested in
    desired_years = [str(year) + '/' + str(year + 1)[-2:] for year in range(2006, 2022)]

    # Now filter the DataFrame to only include the desired years
    data_years_filtered = data_with_years[data_with_years['year'].isin(desired_years)]

    # Reset the index of the DataFrame after filtering
    data_years_filtered.reset_index(drop=True, inplace=True)

    # Filter out rows where the 'gender' column corresponds to 'männlich' (male)
    male_graduates_data = data_years_filtered[data_years_filtered['gender'] == 'männlich']

    # Reset the index of the DataFrame after filtering
    male_graduates_data.reset_index(drop=True, inplace=True)

    # Select every third column starting from 'state_3' to represent the number of male graduates for each state
    # The list comprehension creates a list of column names that we want to sum across
    graduate_columns = ['state_' + str(i) for i in range(3, len(male_graduates_data.columns), 3)]

    male_graduates_data_copy = male_graduates_data.copy()

    # Sum across the selected columns for each year to get the total number of male graduates
    # We do this on the copy to avoid modifying the original DataFrame
    male_graduates_data_copy['total_male_graduates'] = male_graduates_data_copy[graduate_columns].replace('-', 0).astype(int).sum(axis=1)

    # Now we can select only the columns we are interested in: 'actual_year' and 'total_male_graduates'
    graduates = male_graduates_data_copy[['year', 'total_male_graduates']]

    # Slice away the last column
    graduates = graduates.iloc[:-1, :]

    # Repeat each row four times to match quarterly data
    graduates = graduates.loc[graduates.index.repeat(4)].reset_index(drop=True)

    # Slice away the last 3 column
    graduates = graduates.iloc[:-3, :]

    # Create a date range starting from 2007-10-01, for 57 quarters, with quarters starting in October
    quarter_dates = pd.date_range(start='2007-10-01', periods=57, freq='QS-OCT')

    # Assign this new index to the students DataFrame
    graduates.index = quarter_dates

    # Remove the 'year' column
    graduates.drop(columns=['year'], inplace=True)

    # Get the list of columns in the DataFrame
    columns_list = graduates.columns.tolist()
    # Let's say you want to rename the column at index 0
    columns_list[0] = 'Graduates'
    # Assign the modified list of column names back to the DataFrame
    graduates.columns = columns_list

    # Display the final data with total male graduates per year, excluding the year with 0 graduates
    # print(graduates)

    return graduates


def GetGraduatesDataForecast():

    time_series_data = GetGraduatesData()

    # Differencing the series once
    diff_series = time_series_data['Graduates'].diff(1).dropna()

    """
    # Augmented Dickey-Fuller Test (for d)
    result = adfuller(diff_series)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])

    # Partial Autocorrelation Function (PACF) Plot (for p)
    plot_pacf(diff_series, lags=20)
    plt.show()

    # Autocorrelation Function (ACF) Plot (for q)
    plot_acf(diff_series, lags=20)
    plt.show()
    """

    """
    # Fit an ARIMA(1,0,0) model
    # This means: 1 autoregressive term (p=1), no differencing (d=0), and no moving average term (q=0)
    model = ARIMA(diff_series, order=(1, 1, 0))
    model_fit = model.fit()
    """

    # Fit a SARIMA model
    # This means: p=1, d=1, q=0 for non-seasonal order, and P=1, D=1, Q=0 for seasonal order with s=4 (quarterly data)
    # model = SARIMAX(time_series_data['Salary'], order=(1, 1, 0), seasonal_order=(1, 1, 0, 4))
    model = SARIMAX(time_series_data['Graduates'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
    model_fit = model.fit()

    """
    # Summary of the model
    print(model_fit.summary())
    """

    # For forecasting future values you would use:
    forecast = model_fit.forecast(steps=48)  # For forecasting the next 48 periods

    """
    model = ARIMA(time_series_data['Graduates'], order=(p, d, q))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=8) # Forecasting next 5 periods
    """

    plt.figure(figsize=(10, 6))
    plt.plot(time_series_data['Graduates'], label='Historical')
    plt.plot(forecast, label='Forecast')
    plt.legend()
    plt.show()

    plt.close()

    return forecast


GetGraduatesDataForecast()
