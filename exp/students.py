import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX

from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

import os 

def GetStudentsData():
    
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_DIR, "dat")
    STUDENTS_PATH = os.path.join(DATA_DIR, "student_data_per_subject.csv")

    #file_path = '/Users/abdallahabdul-latif/Desktop/Universität Tübingen/5.Semester/Data Literacy/StudentProject/AnalysingStudentDevelopment/data/student_data_per_subject.csv'
    file_path = STUDENTS_PATH

    students = pd.read_csv(file_path, encoding= "ISO-8859-1",sep=";", decimal=".", index_col=0, skiprows=0, skipfooter=0, engine="python")

    # Get the list of columns in the DataFrame
    columns_list = students.columns.tolist()

    # Let's say you want to rename the column at index 2
    columns_list[0] = 'Subject'
    columns_list[1] = 'F'

    # Assign the modified list of column names back to the DataFrame
    students.columns = columns_list

    # Filter the DataFrame for the subject "Informatik" and Fach (F) "HF"
    students = students[students['Subject'] == '"Informatik"']
    students = students[students['F'] == 'HF']

    columns_list = students.columns.tolist()

    # Initialize an empty list to store the indexes of academic year columns
    academic_year_indexes = []

    # Loop through the list of column names
    for i, col_name in enumerate(columns_list):
        # Check if 'WiSe' or 'SoSe' is in the column name, which indicates an academic year
        if 'WiSe' in col_name or 'SoSe' in col_name:
            # If it's an academic year, add the index to our list
            academic_year_indexes.append(i)

    # We will create a new list for the renamed column names
    renamed_columns = []

    renamed_columns.append(columns_list[0])
    renamed_columns.append(columns_list[1])

    # Iterate through the list of academic year indexes
    for i, start_index in enumerate(academic_year_indexes):
        # Add the academic year column name
        renamed_columns.append(columns_list[start_index])
        
        # Determine the end index for this academic year's range of columns
        end_index = academic_year_indexes[i + 1] if i + 1 < len(academic_year_indexes) else len(columns_list)
        
        # Generate the new Fachsemester names for the columns in this range
        for j in range(1, end_index - start_index):
            if j <= 12:
                semester_name = f"Fachsemester_{j}"
            else:
                semester_name = "Fachsemester_>12"
            renamed_columns.append(semester_name)

    # Now you can use 'renamed_columns' to set the column names of your DataFrame
    students.columns = renamed_columns

    # Flatten the DataFrame if it has MultiIndex or hierarchical columns
    students.columns = ['_'.join(map(str, col)) if isinstance(col, tuple) else col for col in students.columns]

    # Iterate through each column
    for col in students.columns:
        if 'Fachsemester' in col:
            # Ensure each column is a Series and then convert to numeric
            column_series = pd.Series(students[col].squeeze())
            students[col] = pd.to_numeric(column_series, errors='coerce')


    for i, index in enumerate(academic_year_indexes):
        # Determine the range of columns for this academic year's Fachsemester
        # Start at the next column after the academic year column and end at the column before the next academic year column
        start = index + 1
        end = academic_year_indexes[i + 1] if i + 1 < len(academic_year_indexes) else len(students.columns)
        
        # Sum the values across these Fachsemester columns
        students.iloc[:, index] = students.iloc[:, start:end].sum(axis=1)

    # Drop all columns that are not academic years or other necessary data
    students = students.iloc[:, academic_year_indexes]

    # Now, we need to drop the 'Fachsemester' columns, keeping only the academic year columns and any other necessary columns
    drop_cols = [col for col in students.columns if 'Fachsemester' in col]
    students.drop(columns=drop_cols, inplace=True)

    # Slice away the first four and last four columns
    students = students.iloc[:, 4:-4]

    # Repeat each semester value to match the quarterly frequency
    # We will repeat each semester's value twice as we transition from semester to quarterly data
    expanded_students = students.apply(lambda x: np.repeat(x, 2))
    expanded_students.reset_index(inplace=True)
    expanded_students.rename(columns={'index': 'Semester', 0: 'Student Count'}, inplace=True)


    # Create a new DataFrame to store the doubled columns
    doubled_columns = pd.DataFrame()

    # Loop through each column and duplicate it
    for col in students.columns:
        doubled_columns[col + '_1'] = students[col]
        doubled_columns[col + '_2'] = students[col]

    # Slice away the first four and last four columns
    doubled_columns = doubled_columns.iloc[:, :-1]

    transposed_students_df = doubled_columns.transpose()


    # Get the list of columns in the DataFrame
    columns_list = transposed_students_df.columns.tolist()
    # Let's say you want to rename the column at index 0
    columns_list[0] = 'Students'
    # Assign the modified list of column names back to the DataFrame
    transposed_students_df.columns = columns_list

    # Create a date range starting from 2007-10-01, for 57 quarters, with quarters starting in October
    quarter_dates = pd.date_range(start='2007-10-01', periods=57, freq='QS-OCT')

    # Assign this new index to the students DataFrame
    transposed_students_df.index = quarter_dates

    # Display the updated DataFrame
    #print(transposed_students_df)

    return transposed_students_df

def GetStudentsDataForecast():

    time_series_data = GetStudentsData()

    # Differencing the series once
    diff_series = time_series_data['Students'].diff(1).dropna()

    
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
    # Fit an ARIMA(1,0,0) model
    # This means: 1 autoregressive term (p=1), no differencing (d=0), and no moving average term (q=0)
    model = ARIMA(diff_series, order=(1, 1, 0))
    model_fit = model.fit()
    """

    # Fit a SARIMA model
    # This means: p=1, d=1, q=0 for non-seasonal order, and P=1, D=1, Q=0 for seasonal order with s=4 (quarterly data)
    #model = SARIMAX(time_series_data['Salary'], order=(1, 1, 0), seasonal_order=(1, 1, 0, 4))
    model = SARIMAX(time_series_data['Students'], order=(1, 0, 0), seasonal_order=(1, 0, 0, 4))
    model_fit = model.fit()

    """ 
    # Summary of the model
    print(model_fit.summary())
    """

    # For forecasting future values you would use:
    forecast = model_fit.forecast(steps=48)  # For forecasting the next 48 periods

    """
    model = ARIMA(time_series_data['Students'], order=(p, d, q))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=8) # Forecasting next 5 periods
    """

    """
    plt.figure(figsize=(10, 6))
    plt.plot(time_series_data['Students'], label='Historical')
    plt.plot(forecast, label='Forecast')
    plt.legend()
    plt.show()

    plt.close()
    
    """

    return forecast


#GetStudentsDataForecast()