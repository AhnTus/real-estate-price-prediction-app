## 1. Import sklearn Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')

"""## 2. Import Dataset"""

mum_prop = pd.read_csv('Final_Project.csv')
mum_prop

"""## 3. Data Understanding"""

mum_prop.shape

mum_prop.info()

mum_prop.isna().sum()

mum_prop.describe().round()

"""## 4. Feature Engineering

### 4.1 Drop Unwanted Columns
"""

mum_prop.head()

mum_prop.drop(columns=['Property_Name', 'Location','Availability','Bathroom'], inplace =  True)
print('Shape of data :', mum_prop.shape)

"""### 4.2 Label Encoding for Categorical Columns"""

le = LabelEncoder()

for column in mum_prop.describe(include='object').columns:
    mum_prop[column] = le.fit_transform(mum_prop[column])

mum_prop.describe().round(2).T

mum_prop

mum_prop.info()

"""### 4.3 Looking for Minimum & Maximum"""

for i in mum_prop.columns:
    print(i,'Min value :', mum_prop[i].min(),'Max value :', mum_prop[i].max())

"""### 4.4 Correlation Heatmap"""

fig = plt.figure( figsize =(9,8))
rcParams = {'xtick.labelsize':'14','ytick.labelsize':'14','axes.labelsize':'16'}
sns.heatmap(mum_prop.corr(),annot = True, linewidths=.5, cbar_kws={"shrink": .5},fmt='.2f', cmap='coolwarm')
fig.suptitle('Heatmap Mumbai Property Data',fontsize=18, fontweight="bold")
pylab.rcParams.update(rcParams)
fig.tight_layout()
plt.show()

fig.savefig('Heatmap_Encoding', dpi = 250)

"""## 5. Model Building"""

mum_prop.head()

"""### 5.1 Train Test Split"""

X =  mum_prop.drop('Price_Lakh', axis = 1)
y =  mum_prop['Price_Lakh']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.20, random_state = 12)

print(X_train.shape, X_test.shape)

"""### 5.2 Linear Regression"""

from sklearn.linear_model import LinearRegression

linear = LinearRegression()
linear.fit(X_train, y_train)

print("Training Accuracy = ", linear.score(X_train, y_train))
print("Test Accuracy     = ", linear.score(X_test, y_test))

"""### 5.3 Decision Tree Regressor"""

from sklearn.tree import DecisionTreeRegressor

dt = DecisionTreeRegressor(min_samples_split=2)
dt.fit(X_train, y_train)

print("Training Accuracy = ", dt.score(X_train, y_train))
print("Test Accuracy     = ", dt.score(X_test, y_test))

"""### 5.4 Random Forest Regressor"""

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators = 1000, max_depth=5, random_state = 12)
rf.fit(X_train, y_train);

print("Training Accuracy = ", rf.score(X_train, y_train))
print("Test Accuracy     = ", rf.score(X_test, y_test))

"""### 5.5 Polynomial Features"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2)
poly.fit_transform(X)

# Define the pipeline and train model
poly_model = Pipeline([('poly', PolynomialFeatures(degree=2)),
                       ('rf', RandomForestRegressor(n_estimators = 1000, max_depth=5, random_state = 12))])
poly_model.fit(X_train, y_train)

# Calculate the Score
print("Training Accuracy = ", poly_model.score(X_train, y_train))
print("Test Accuracy     = ", poly_model.score(X_test, y_test))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2)
poly.fit_transform(X)

# Define the pipeline and train model
poly_model = Pipeline([('poly', PolynomialFeatures(degree=2)), ('linear', LinearRegression(fit_intercept=False))])
poly_model.fit(X_train, y_train)

# Calculate the Score
print("Training Accuracy = ", poly_model.score(X_train, y_train))
print("Test Accuracy     = ", poly_model.score(X_test, y_test))

"""## Obeservaion :
### 1. We select the final model - Polynomial Feature.
### 2. We got 98.73 % Model Accuracy.

## 6. Final Model Evaluation
"""

def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    errors = abs(predictions - test_labels)
    accuracy = model.score(test_features, test_labels)

    print('Average Error  = {:0.4f} degrees'.format(np.mean(errors)))
    print('Model Accuracy = {:0.4f} %'.format(accuracy))

evaluate(poly_model, X_train, y_train)

evaluate(poly_model, X_test, y_test)

"""### 6.1 Visualizing Results"""

pred = poly_model.predict(X_test)

fig = plt.figure(figsize=(8,7))

sns.scatterplot(y_test, pred)
fig.suptitle('Prediction using Polynomial', fontsize= 18 , fontweight='bold')
plt.xlabel("Actual")
plt.ylabel("Prediction")
pylab.rcParams.update(rcParams)
fig.tight_layout()
fig.subplots_adjust(top=0.92)
plt.show()

#fig.savefig('Prediction_Polynomial', dpi = 500)

"""## 7. Model Deployement"""

from pickle import dump

dump(poly_model,open('regression_model.pkl','wb'))

"""# The End !!!"""