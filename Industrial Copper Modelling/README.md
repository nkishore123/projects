Title
# Indusrial Copper Modelling
## Problem Statement:
The copper industry deals with less complex data related to sales and pricing. However, this data may suffer from issues such as skewness and noisy data, which can affect the accuracy of manual predictions. 
Dealing with these challenges manually can be time-consuming and may not result in optimal pricing decisions. A machine learning regression model can address these issues by utilizing advanced techniques such as data normalization, feature scaling, and outlier detection, and leveraging algorithms that are robust to skewed and noisy data.
Another area where the copper industry faces challenges is in capturing the leads. A lead classification model is a system for evaluating and classifying leads based on how likely they are to become a customer . 
You can use the STATUS variable with WON being considered as Success and LOST being considered as Failure and remove data points other than WON, LOST STATUS values.

## Approach:
1) Data Understanding: First we need to understand the data and the datatypes.
2) Data Preprocessing:
● Handle missing values with mean/median/mode.
● Treat Outliers using IQR.
● Identify Skewness in the dataset and treat skewness with appropriate data transformations, such as log transformation to handle high skewness in continuous variables.
● Encode categorical variables using suitable techniques, such as one-hot encoding, label encoding, or ordinal encoding, based on their nature and relationship with the target variable.
3) EDA: Try visualizing outliers and skewness using Seaborn’s boxplot, distplot, violinplot.
4) Feature Engineering: Engineer new features if applicable, such as aggregating or transforming existing features to create more informative representations of the data. And drop highly correlated columns using SNS HEATMAP.
5) Model Building and Evaluation:
● Split the dataset into training and testing/validation sets.
● Train and evaluate different classification models, see the classifier performance using appropriate evaluation metrics such as accuracy, precision, recall, F1 score, and AUC curve.
● Optimize model hyperparameters using techniques such as cross-validation and grid search to find the best-performing model.
● Interpret the model results and assess its performance based on the defined problem statement.
● Same steps for Regression modelling.
6) Model GUI: Using streamlit module, create interactive page to take inputs from the user and predict the output.
