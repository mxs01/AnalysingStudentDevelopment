import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import salaries
import students
import graduates

import matplotlib.pyplot as plt


# Load your datasets
salaries_data = salaries.GetSalaryData()
graduates_data = graduates.GetGraduatesData()
students_data = students.GetStudentsData()

""""
print(salaries_data.shape)
print(graduates_data.shape)
print(students_data.shape)
"""

# Combine datasets into a single DataFrame (assuming they are all aligned and sorted by date)
combined_data = pd.DataFrame({
    'salaries': salaries_data['Salary'],
    'graduates': graduates_data['Graduates'],
    'students': students_data['Students']
})

# Define features and target variable
X = combined_data[['salaries', 'graduates']]  # Features
y = combined_data['students']  # Target

# Split data into training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
error = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {error}")

# Assuming df is your DataFrame and 'target' is the column with your target variable
# Replace 'target' with the actual name of your target variable column

# Calculate the standard deviation of the target variable
target_std = students_data['Students'].std()

# Display the standard deviation
print("Standard Deviation of Target Variable:", target_std)


# For forecasting future student numbers, you would predict using new salary and graduates data:
future_salaries = salaries.GetSalaryDataForecast()
future_graduates = graduates.GetGraduatesDataForecast()
future_students_pred = model.predict(pd.DataFrame({'salaries': future_salaries, 'graduates': future_graduates}))


# Create a DataFrame combining the input data and predictions
prediction_df = pd.DataFrame({
    'Salaries': future_salaries,
    'Graduates': future_graduates,
    'Predicted Students': future_students_pred
})

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(prediction_df['Predicted Students'], label='Predicted Students', color='blue')
plt.xlabel('Time')
plt.ylabel('Number of Students')
plt.title('Predicted Number of Students Over Time')
plt.legend()

# Optional: Plot salaries and/or graduates on a secondary axis
ax2 = plt.gca().twinx()
ax2.plot(prediction_df['Salaries'], label='Salaries', color='green', linestyle='--')
ax2.set_ylabel('Salaries')
ax2.legend(loc='upper left')

plt.show()
