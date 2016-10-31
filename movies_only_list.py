# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:13:01 2016

@author: sonia
"""
import pandas as pd

yr= 2016
file_name = 'imdb_list_' + str(yr) + '.csv' # filename to be read
df = pd.read_csv(file_name)  # read the file with movies and series list
movie_year = '('+str(yr)+')' 
movies_only_df = df[df['release_year']==movie_year] # subset the df to only movies excluding series, TVmovies, miniseries etc.

# repeat the process for each year and append the data frame
for yr in reversed(range(2005, 2017)):
    file_name = 'imdb_list_' + str(yr) + '.csv'
    df = pd.read_csv(file_name)
    movie_year = '('+str(yr)+')'
    df_next = df[df['release_year']==movie_year]
    movies_only_df = pd.concat([movies_only_df, df_next])
    print('size of the data frame after year',yr ,'is',movies_only_df.shape[0])
    
    
movies_only_df.to_csv('movies_only_list.csv')

