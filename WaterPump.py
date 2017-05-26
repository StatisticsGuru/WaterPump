# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:14:09 2017

@author: a-mlinets
"""

# Import Libraries
import pandas as pd
from patsy import dmatrices
import matplotlib as plt
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Import Data
# Define train_values_url
train_values_url = "http://s3.amazonaws.com/drivendata/data/7/public/4910797b-ee55-40a7-8668-10efd5c1b960.csv"
train_labels_url = "http://s3.amazonaws.com/drivendata/data/7/public/0bf8bc6e-30d0-4c50-956a-603fc693d966.csv"
test_values_url = "http://s3.amazonaws.com/drivendata/data/7/public/702ddfc5-68cd-4d1d-a0de-f5f566f76d91.csv"

# Read data into pandas data frames
trainvalues = pd.read_csv(train_values_url)
trainlabel = pd.read_csv(train_labels_url)
testvalues = pd.read_csv(test_values_url)

# Merge into a single dataframe
WaterPumps = trainvalues.merge(trainlabel, on='id')

# Data Summary: Look at what we have in the data frame
WaterPumps.describe() # provides summary of the numerical variables
WaterPumps.dtypes # provides data types, 'object' is character type
WaterPumps.head(10) #first 10 rows of the data 

WaterPumps['status_group'].value_counts() # returns count of categories

# VISUALIZTIONS:  Add fancy plots
WaterPumps.boxplot(column='population', by='waterpoint_type_group')

""" DATA MANIPULATION WITH PANDAS - LEARNING"""""""""""""""""""""""""""""

# Boolean Indexing: get all status_groups where source is spring
WaterPumps.loc[WaterPumps['source']=='spring',['status_group']]

# CrossTab - Levels
ct = pd.crosstab(WaterPumps['source'],WaterPumps['status_group'], margins=True)
ct.plot(kind='bar', stacked=True, grid=False)
# CrossTab - Percentages
def percConvert(ser):
    return ser/float(ser[-1])
ctp = pd.crosstab(WaterPumps['status_group'], WaterPumps['source'], margins=True).apply(percConvert, axis=1)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Categorical Data Analysis: Find all missing values
WaterPumps.apply(lambda x: sum(x.isnull()), axis=0)

"""Preprocessing"""
#Drop categorical variables with too many levels
keepvarindex = [x for x,y in enumerate(WaterPumps.dtypes) if y=='object' and 
len(pd.Series(WaterPumps.iloc[:,x]).unique())<30 or y!='object']

WaterPumps = WaterPumps.ix[:,keepvarindex]
# Drop NAs
WaterPumps.dropna(axis=0, inplace=True)
# Drop columns that aren't predictive of the outcome
WaterPumps.drop(['id','recorded_by'], axis=1, inplace=True)

# Convert all categorical variables into numeric
le=LabelEncoder()
for i in [x for x,y in enumerate(WaterPumps.dtypes) if y =='object']:
    # Encode missing values as NaN (otherwise encoder will break)
    # WaterPumps.iloc[:,i][pd.isnull(WaterPumps.iloc[:,i])]='NaN'
    WaterPumps.iloc[:,i]=le.fit_transform(pd.Series(WaterPumps.iloc[:,i]))
WaterPumps.dtypes

# Select character columns from the dataset
#WaterPumps_char = WaterPumps[[x for x,y in enumerate(WaterPumps.dtypes) if y =='object']]

# Convert character data frame into design matrix
#formula = 'status_group~'+('+'.join(WaterPumps_char.columns.difference(['status_group'])))
#y_train, X_train = dmatrices("status_group~payment_type", WaterPumps_char)
































