# -*- coding: utf-8 -*-
"""B15 - Employee Attrition Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zqfmVPh9mjVQ8xEsDQPbCea6dTa_cfd8

# Import Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder as le
from sklearn.metrics import f1_score, classification_report
from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_auc_score, accuracy_score

"""# Data Extraction"""

attrition_data = pd.read_csv('/content/sample_data/Train.csv') #reading data

attrition_data.head() #printing first five rows

attrition_data.shape #(rows, columns)

attrition_data.isnull().any() #checking if columns has null vlaues

"""# Data Preprocessing
###Fill Missing Values
"""

null_columns = [] #filtering out columns which has null values
for col in attrition_data.columns:
  if attrition_data[col].isnull().any() == True:
    null_columns.append(col)
null_columns

def fillNullValues(data,col): # function to fill up null values
  data[col].fillna((data[col].mean()),inplace=True)

for col in null_columns:  #populating all the null columns
  fillNullValues(attrition_data,col)

attrition_data.isnull().any()

Attrition = list(attrition_data['Attrition_rate'].round(decimals=0)) #rounding off attrition value to 0 or 1

attrition_data['Attrition'] = Attrition  #inserting new column into dataframe
attrition_data['Attrition'] = le().fit_transform(attrition_data['Attrition'])

"""### Correlation"""

attrition_data.corr()

plt.figure(figsize= (15,15))
sns.heatmap(attrition_data.corr(), annot=True, fmt = '.0%')
plt.show()
plt.close()

"""### Label Encoding"""

#Label encoding to convert words to numeric values
for col in attrition_data.columns:
  if attrition_data[col].dtype == 'int64'or attrition_data[col].dtype == 'float64':
    continue
  else:
    attrition_data[col] = le().fit_transform(attrition_data[col])

attrition_data.head() #printing first five rows

attrition_data.info()

"""###Dropping Column"""

attrition_data = attrition_data.drop(['Employee_ID'], axis = 1) #dropping columns which doesnot impact attrition
attrition_data.head()

"""### *OverSampling of data*"""

attrition_data['Attrition'].value_counts()

X = attrition_data.drop(['Attrition', 'Attrition_rate'], axis = 1)
Y = attrition_data['Attrition']
print(X.shape, Y.shape)

from imblearn import over_sampling
from imblearn.over_sampling import RandomOverSampler
from collections import Counter

ros = RandomOverSampler(random_state=0)
x_resampled, y_resampled = ros.fit_resample(X, Y)

"""### Model Building"""

X_train, X_test, y_train, y_test = train_test_split(x_resampled, y_resampled, test_size=0.25, random_state=42) #splitting into train and test data

X_train.shape, X_test.shape, y_train.shape, y_test.shape

from sklearn.preprocessing import StandardScaler 
sc = StandardScaler() 
X_train = sc.fit_transform(X_train) 
X_test = sc.transform(X_test)

from sklearn.neighbors import KNeighborsClassifier

train_acc_list = [] #to find which k value brings high accuracy
test_acc_list = []
k_range = range(1, 11)
for k in k_range:    
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred_train = knn.predict(X_train)
    y_pred_test = knn.predict(X_test)
    train_acc_list.append(accuracy_score(y_train, y_pred_train))
    test_acc_list.append(accuracy_score(y_test, y_pred_test))
    print(k)
    print('Test:', accuracy_score(y_test, y_pred_test))
    print('Train:', accuracy_score(y_train, y_pred_train))
    print('--------------------------------------------')

knn = KNeighborsClassifier(n_neighbors=1) #training the model with k = 1
knn.fit(X_train, y_train)
Y_pred_test = knn.predict(X_test)
Y_pred_train = knn.predict(X_train)
print(accuracy_score(y_train, Y_pred_train))
print(accuracy_score(y_test, Y_pred_test))

"""### Test Data"""

attrition_test_data = pd.read_csv('/content/sample_data/Test.csv') #reading test data

"""### Filling NULL values"""

null_columns_test = [] #filling up null values
for col in attrition_test_data.columns:
  if attrition_test_data[col].isnull().any() == True:
    null_columns_test.append(col)
null_columns_test

for col in null_columns_test:
  fillNullValues(attrition_test_data,col)

"""### Label Encoding for test data"""

for col in attrition_test_data.columns: #label encoding
  if attrition_test_data[col].dtype == 'int64'or attrition_test_data[col].dtype == 'float64':
    continue
  else:
    attrition_test_data[col] = le().fit_transform(attrition_test_data[col])

attrition_test_data.head()

Emp_ID = (attrition_test_data['Employee_ID'])
print(Emp_ID)

attrition_test_data = attrition_test_data.drop(['Employee_ID'], axis = 1) #dropping employee id column

test_preds=knn.predict(attrition_test_data) #predicting

df_preds=pd.DataFrame()
df_preds["Attrition_rate"] = test_preds 
df_preds["EMP_ID"] = Emp_ID
df_preds

df_preds["Attrition_rate"].value_counts()

print(df_preds[df_preds['Attrition_rate'] == 1]) #printing all rows numbers with attrition 1

from google.colab import drive
drive.mount('drive')

df_preds.to_csv('data.csv')
!cp data.csv "drive/My Drive/"



from google.colab import drive
drive.mount('/content/drive')

