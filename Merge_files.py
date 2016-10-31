# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 20:42:23 2016

@author: sonia
"""

### Combine the data into a single file
import pandas as pd


df1= pd.read_csv('movie_data1_131_New.csv')
df2=pd.read_csv('movie_data132_169_New.csv')
df3 = pd.read_csv('movie_data132_209_New.csv')
df4= pd.read_csv('movie_data210_293_New.csv')
df5= pd.read_csv('movie_data295_388_New.csv')
df6= pd.read_csv('movie_data390_508_New.csv')
df7= pd.read_csv('movie_data509_18608_New.csv')
df8= pd.read_csv('movies_dataF_New.csv')

df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8])
df.to_csv('Movies.csv')
