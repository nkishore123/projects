# Customer Lead Prediction

## Problem Statement
The online Edu-Tech platform that generates leads through various sources. The marketing and sales
teams want to optimize their lead conversion rates and improve the efficiency of their lead management
process. The primary goal is to predict whether a lead will be successfully converted into a customer or
not. This prediction can help the Edu-Tech company to prioritize leads with the highest conversion
potential and tailor marketing and sales strategies accordingly. The analysis and prediction will be
based on the information available in the provided dataset.

## Approach
1. Remove unwanted columns Like Id.
2. There are so many null values. Filling the null values with median or mode will make that particular value dominant than other values. So, we need to fill null values with a random value from that column.
3. Checking unique values in each categorical column to check the values.
4. Some Columns have dominant category (Ex: out of 100 datapoints, “Yes” has 98 and “No” has 2. We can remove them.
5. Replacing the “SELECT” with random value from the particular column.
6. Label Encoding the columns which have ordinal type of data
7. One Hot encoding columns which are type of nominal data.
8. Converting all the values to numpy array to create a model.
