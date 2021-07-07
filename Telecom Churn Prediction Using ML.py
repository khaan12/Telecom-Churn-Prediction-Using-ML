# -*- coding: utf-8 -*-
"""python training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iuZpsv99_P2_IybJBqgvHaWTrKXnIRUL

# welcome to our fyp project

# All the libraries are included here
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,plot_roc_curve,plot_precision_recall_curve
from sklearn import tree



from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.gaussian_process.kernels import RBF

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import  AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier
import seaborn as sns











"""# load dataset 

"""

dataset = pd.read_csv("churn-bigml-20.csv")

from google.colab import drive
drive.mount('/content/drive')

dataset.shape

"""# visualization of dataset

----checking null values-----
"""

missing_data=dataset.isnull()
for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print("")
# Looking at data types
dataset.dtypes

dataset.head(3)

dataset.info()

dataset.isnull().sum()



"""converting bool datatype colum to int """

dummy = pd.get_dummies(dataset['Voice mail plan'])

dummy.head()

data = pd.concat((dataset,dummy),axis=1)

data =data.drop(['No'],axis=1)

data =data.drop(['Voice mail plan'],axis=1)
data =data.rename(columns={"Yes":"Voice mail plan"})

data.head()

dummy2 = pd.get_dummies(data['International plan'])

set1 = pd.concat((data,dummy2),axis=1)

set1 =set1.drop(['No'],axis=1)

set1 =set1.drop(['International plan'],axis=1)

set1 =set1.rename(columns={"Yes":"International plan"})

set1.head()

"""#five no summary

"""

set1.describe()

set1.loc[dataset['Total day charge']>30,'Churn']







col_name="Churn"
first_col = set1.pop(col_name)

set1.insert(19, col_name, first_col)

set1.head()













set1['Churn'].unique()



X = set1.iloc[:,1:18].values
yy  = set1.iloc[:,1:18]
Y= set1.iloc[:,19].values

yy

for col in yy.columns: 
    try:      
        yy[col] = pd.to_numeric(yy[col]) 
        yy.hist(column=col)
    except ValueError:
        print('This column can not be represented as a histogram')

X



Y

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2,random_state=0)



from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train= sc.fit_transform(x_train)

x_test= sc.transform(x_test)

"""#random forest"""

clf = RandomForestClassifier(n_estimators=20)
clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)

confusion_matrix(y_test,y_pred)

classification_report(y_test,y_pred)

accuracy_score(y_test,y_pred)

# looking at the importance of each feature
importances= clf.feature_importances_
for i,v in enumerate(importances):
	print('Feature: %0d, Score: %.5f' % (i,v))

# visualize to see the feature importance
indices=np.argsort(importances)[::-1]
plt.figure(figsize=(20,10))

plt.bar( range(len(clf.feature_importances_)), clf.feature_importances_)
plt.xticks(range(len(clf.feature_importances_)), yy.columns)
plt.show()

pd.Series(clf.feature_importances_, index=yy.columns)
   .nlargest(5)
   .plot(kind='bar')

plt.bar( range(len(clf.feature_importances_)), clf.feature_importances_)
plt.xticks(range(len(clf.feature_importances_)), set1.columns)
plt.figure(figsize=(20,10))
plt.show()

"""#decession tree



"""

DT = tree.DecisionTreeClassifier()

DT.fit(x_train,y_train)

y_pred_dt= DT.predict(x_test)

confusion_matrix(y_test,y_pred_dt)

classification_report(y_test,y_pred_dt)

accuracy_score(y_test,y_pred_dt)



"""#curves

"""

plot_roc_curve(DT,x_test,y_test)

plot_precision_recall_curve(DT,x_test,y_test)

plot_roc_curve(clf,x_test,y_test)

plot_precision_recall_curve(clf,x_test,y_test)

names = ["Nearest_Neighbors", "Linear_SVM", "Polynomial_SVM", "RBF_SVM", "Gaussian_Process",
         "Gradient_Boosting", "Extra_Trees", "Neural_Net", "AdaBoost",
         "Naive_Bayes", "QDA", "SGD"]

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(kernel="poly", degree=3, C=0.025),
    SVC(kernel="rbf", C=1, gamma=2),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0),
    
    ExtraTreesClassifier(n_estimators=10, min_samples_split=2),
    
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(n_estimators=100),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
    SGDClassifier(loss="hinge", penalty="l2")]

scores = []
for name, clf in zip(names, classifiers):
    clf.fit(x_train, y_train)
    score = clf.score(x_test, y_test)
    scores.append(score)

df = pd.DataFrame()
df['name'] = names
df['score'] = scores
df['percentage']=100*df['score']
df

cm = sns.light_palette("green", as_cmap=True)
s = df.style.background_gradient(cmap=cm)
s

sns.set(style="whitegrid")
ax = sns.barplot(y="name", x="score", data=df)

import matplotlib.pyplot as plotter
figureObject, axesObject = plotter.subplots()
mylabels = df.name
y=df.score
axesObject.axis('equal')
axesObject.pie(y,
        labels = mylabels,
        radius=2.5,
        
        autopct='%0.1f%%')
plotter.legend(title = "Algorithms scores:",loc='center')
plotter.show()