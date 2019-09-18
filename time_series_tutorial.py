#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:23:41 2019
@author: janicelove
"""

#Time series Data Visualization with Python
#Tutorial: https://machinelearningmastery.com/time-series-data-visualization-with-python/

"""About the dataset:
    -minimum daily temperatures over 10 years (1981-1990) for Melbourne, Australia
    -SOURCE: Australian Burean of Meterology
    -NOTE: temperatures are Celsius
"""
#import packages
import pandas as pd 
from matplotlib import pyplot 

#import data
series = pd.read_csv('/home/janicelove/Desktop/DataSci/Time_series_visualization/daily-min-temperatures.csv', 
                     header=0, index_col=0, parse_dates=True, squeeze=True)

#Time series line plot 
series.plot()
pyplot.show()

#Change the style:
series.plot(style='k.')
pyplot.show()

#Exploring data: grouping by year, visualization
groups = series.groupby(pd.Grouper(freq='A'))
years = pd.DataFrame()
for name, group in groups:
    years[name.year] = group.values
years.plot(subplots=True, legend=False)
pyplot.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
pyplot.show()

#Time series Histogram and Density Plots: Gaussian distribution 
series.hist()
series.plot(kind='kde')

#Time series box and whisker plots by interval 
years.boxplot()

one_year = series['1990']
groups = one_year.groupby(pd.Grouper(freq='M'))
months = pd.concat([pd.DataFrame(x[1].values) for x in groups], axis=1)
months = pd.DataFrame(months)
months.columns=range(1,13)
months.boxplot()

#Time series heat maps
#creating a matrix of year-columns and day-rows, each cell is minimum temperature for the day 
#TRANSPOSED: each row represents one year and each column is one day for more intuitive layout
groups = series.groupby(pd.Grouper(freq='A'))
years = pd.DataFrame()
for name, group in groups:
    years[name.year] = group.values
years=years.T
pyplot.matshow(years, interpolation=None, aspect='auto')

#heat map for one year, 1990
one_year=series['1990']
groups = one_year.groupby(pd.Grouper(freq='M'))
months=pd.concat([pd.DataFrame(x[1].values) for x in groups], axis=1)
months =pd.DataFrame(months)
months.columns = range(1,13)
pyplot.matshow(months, interpolation=None, aspect='auto')
pyplot.show()

#Time series lag scatter plots
"""Time series modeling assumes a relationship between an observation and the previous one
    - Lags: DEF-previous observations
    - pandas built-in function called lag plot: plots observation at t (x-axis) and lag (t-1) on y-axis 
        -can show positive or negative relationships, points tight to the diagonal means stronger relationship and 
        points further from line suggest weaker relationship 
        - a ball in the middle or spread across plot: no relationship or a weak one 
"""
#create a scatterplot for each observation in previous 7 days
values=pd.DataFrame(series.values)
lags=7
columns=[values]
for i in range(1,(lags+1)):
    columns.append(values.shift(i))
dataframe=pd.concat(columns,axis=1)
columns=['t+1']
for i in range(1,(lags+1)):
    columns.append('t-' + str(i))
dataframe.columns=columns
pyplot.figure(1)
for i in range(1,(lags+1)):
    ax=pyplot.subplot(240+i)
    ax.set_title('t+1 vs t-' +str(i))
    pyplot.scatter(x=dataframe['t+1'].values, y=dataframe['t-'+str(i)].values)
pyplot.show()
#Results: strongest correlation with t-1 value, but correlated values throughout week   

#time series autocorrelation plots
"""
Correlation: DEF-To quantify the strength and type of relationship between observations
    -in time series, when correlation is calculated against its lag values it is called autocorrelation  
Correlation values are calculated betweeb 1 and 0, +/- is for postive/negative correlations, values close to 0
are weak correlations and those close to 1 are strong. aka correlation coefficients
"""

from pandas.plotting import autocorrelation_plot
autocorrelation_plot(series)
pyplot.show()      
#sine waves are a strong correlation of seasonality in the dataset
