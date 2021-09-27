import pandas as pd
import numpy as np
from sklearn import linear_model
import pickle


df = pd.read_csv('diabetes.csv')

# Check for null values
# print(df.isnull().sum()) # No null values

reg = linear_model.LinearRegression()

reg.fit(df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']], df.Outcome)

#print(reg.predict([[2, 148, 72, 35, 0, 33.6, 0.627, 50]]))

test_pred = reg.predict([[2, 148, 72, 35, 0, 33.6, 0.627, 50]])

test_pred_rounded = np.round(test_pred[0], 2) # Round to 2 dp

#print(test_pred_rounded)

pickle.dump(reg, open('diabetes.pkl', 'wb'))

pickled_model = pickle.load(open('diabetes.pkl', 'rb'))

