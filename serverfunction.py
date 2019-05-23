import boto3

import pandas as pd

import csv
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import  linear_model

from sklearn.model_selection import train_test_split

######it's key of yours
yourkeyid='something'
yoursecretkeyid='something'

#return the dataset from the dynamodb
def getdata():
	dynamodb = boto3.resource('dynamodb',
	    aws_access_key_id=yourkeyid,
	    aws_secret_access_key=yoursecretkeyid,
	    region_name='us-east-1')
	table = dynamodb.Table('iotcurrent')


	item=table.scan()['Items'][0]
	test=[[item['time'],item['co2'],item['delay']]]
	return test


#build a random forest classifier

def rf():

	data = pd.read_csv("data.csv") 
	x=data[['time','co2','delay']]
	y=data['people']>=10

	# In[100]:


	clf = RandomForestClassifier(n_estimators=100, max_depth=10,random_state=0)
	clf.fit(x, y)
	return clf

#return a linear regresssion
def lg():

	data = pd.read_csv("data.csv") 
	x=data[['time','co2','delay']]
	y=data['people']
	regr = linear_model.LinearRegression()
	regr.fit(x,  y)
	return regr






