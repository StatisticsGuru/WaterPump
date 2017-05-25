# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:14:09 2017

@author: a-mlinets
"""

# Import Libraries
import pandas as pd
import patsy

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

# Convert data frame into design matrix
formula = 'status_group~'+('+'.join(WaterPumps.columns-['status_group']))
print(formula)
y_train, X_train = patsy(formula=formula, WaterPumps)
