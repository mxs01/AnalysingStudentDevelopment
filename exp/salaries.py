import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

import os 

def GetSalaryData():

    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_DIR, "dat")
    GRADUATES_PATH = os.path.join(DATA_DIR, "sallary_per_sector.csv")

    #file_path = '/Users/abdallahabdul-latif/Desktop/Universität Tübingen/5.Semester/Data Literacy/StudentProject/AnalysingStudentDevelopment/data/sallary_per_sector.csv'
    file_path = GRADUATES_PATH
    data = pd.read_csv(file_path, encoding= "ISO-8859-1",sep=";", decimal=".", skiprows=5, skipfooter=9, index_col=0, engine="python")

    # Get the list of columns in the DataFrame
    columns_list = data.columns.tolist()

    # Let's say you want to rename the column at index 2
    columns_list[0] = 'sector'
    columns_list[1] = 'year'
    columns_list[2] = 'quarter'
    columns_list[3] = 'salary'
    columns_list[6] = 'salary'

    # Assign the modified list of column names back to the DataFrame
    data.columns = columns_list

    # The value you're looking for
    specific_value = 'Forschung und Entwicklung'

    # Create a new DataFrame with only the rows where 'sector' column has the specific value
    filtered_data = data[data['sector'] == specific_value].copy()

    # Creating a new DataFrame with only the first five columns of the filtered_data DataFrame
    new_data_with_five_columns = filtered_data.iloc[:, :7].copy()

    new_data_with_five_columns_male = new_data_with_five_columns.iloc[:, :4].copy()
    new_data_with_five_columns_female = new_data_with_five_columns.iloc[:, [0, 1, 2, -1]]

    # Preprocess year column
    new_data_with_five_columns_male['year'] = new_data_with_five_columns_male['year'].astype(int)
    new_data_with_five_columns_female['year'] = new_data_with_five_columns_female['year'].astype(int)

    # Preprocess the 'quarter' column to standard format
    # Assuming the original format is something like '1. Quartal', '2. Quartal', etc.
    new_data_with_five_columns_male['quarter'] = new_data_with_five_columns_male['quarter'].str.extract('(\d)').astype(str)
    new_data_with_five_columns_female['quarter'] = new_data_with_five_columns_female['quarter'].str.extract('(\d)').astype(str)

    # Now create the 'date' column
    new_data_with_five_columns_male['date'] = pd.to_datetime(new_data_with_five_columns_male['year'].astype(str) + 'Q' + new_data_with_five_columns_male['quarter'])
    new_data_with_five_columns_female['date'] = pd.to_datetime(new_data_with_five_columns_female['year'].astype(str) + 'Q' + new_data_with_five_columns_female['quarter'])

    # Reset the index of the DataFrame
    new_data_with_five_columns_male.reset_index(drop=True, inplace=True)
    new_data_with_five_columns_female.reset_index(drop=True, inplace=True)

    # Assuming your DataFrame is named 'new_data_with_five_columns'
    # Ensure 'date' is a datetime and 'salary' is numeric
    new_data_with_five_columns_male['date'] = pd.to_datetime(new_data_with_five_columns_male['date'], errors='coerce')
    new_data_with_five_columns_male['salary'] = pd.to_numeric(new_data_with_five_columns_male['salary'], errors='coerce')

    new_data_with_five_columns_female['date'] = pd.to_datetime(new_data_with_five_columns_female['date'], errors='coerce')
    new_data_with_five_columns_female['salary'] = pd.to_numeric(new_data_with_five_columns_female['salary'], errors='coerce')

    # Drop rows where 'date' or 'salary' is NaN
    new_data_with_five_columns_male.dropna(subset=['date', 'salary'], inplace=True)
    new_data_with_five_columns_female.dropna(subset=['date', 'salary'], inplace=True)

    # Extract the 'date' and 'salary' columns as NumPy arrays
    dates_male = new_data_with_five_columns_male['date'].to_numpy()
    salaries_male = new_data_with_five_columns_male['salary'].to_numpy()

    # Assuming dates_male is an array of dates
    dates_male = pd.to_datetime(dates_male)

    # Assuming salaries_male is an array of salary values
    time_series_data = pd.DataFrame({'Salary': salaries_male}, index=dates_male)

    # Slice away the last column
    time_series_data = time_series_data.iloc[3:, :]

    #print(time_series_data)

    return time_series_data


def GetSalaryDataForecast():

    time_series_data = GetSalaryData()

    # Differencing the series once
    diff_series = time_series_data['Salary'].diff(1).dropna()


    # Tests for finding hyperparameter p,d and q

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
    #model = SARIMAX(time_series_data['Salary'], order=(1, 1, 0), seasonal_order=(1, 1, 0, 4))
    model = SARIMAX(time_series_data['Salary'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 4))
    model_fit = model.fit()

    """ 
    # Summary of the model
    print(model_fit.summary())
    """

    # For forecasting future values you would use:
    forecast = model_fit.forecast(steps=48)  # For forecasting the next 48 periods

    """
    model = ARIMA(time_series_data['Salary'], order=(p, d, q))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=8) # Forecasting next 5 periods
    """

    """
    plt.figure(figsize=(10, 6))
    plt.plot(time_series_data['Salary'], label='Historical')
    plt.plot(forecast, label='Forecast')
    plt.legend()
    plt.show()

    plt.close()
    """

    return forecast



#GetSalaryData()
