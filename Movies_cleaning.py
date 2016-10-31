# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 07:26:11 2016

@author: sonia
"""

import pandas as pd
import numpy as np
from datetime import datetime

df =pd.read_csv('Movies.csv')

df.drop(df.columns[0:3], axis=1, inplace =True) # remove first three columns

df2 = df.drop_duplicates() # remove duplicate rows

df2.loc[:, 'gross_revenue'] 

#def strip_func(df, column_name):
#    df.column_name = [x.strip() for x in df.column_name.values]
    
df2.gross_revenue = [x.strip() for x in df2.gross_revenue.values]
df2.budget = [str(x).strip('$') for x in df2.budget.values]
df2.tag_lines = [str(x).strip() for x in df2.tag_lines.values]
df2.plot_summary = [str(x).strip() for x in df2.plot_summary.values]
df2.opening_weekend_revenue = [str(x).strip( '(UK') for x in df2.opening_weekend_revenue.values]
df2.opening_weekend_revenue = [str(x).strip('$') for x in df2.opening_weekend_revenue]
df2.gross_revenue = [str(x).strip('$') for x in df2.gross_revenue]

# rearrange columns
cols = df2.columns.tolist() # get a list of column names
cols = np.array([cols[19] , cols[15], cols[4], cols[21], cols[0], cols[5], cols[11], cols[12], cols[18], cols[14], cols[13], cols[16], cols[2], cols[3], cols[17], cols[8], cols[20], cols[1], cols[9], cols[10], cols[7], cols[6]]) # reorder

df2 = df2.ix[:, cols]
df2['id']=range(1, df2.shape[0]+1) # create id column

df2.to_csv('Movies_clean.csv')


##### 

df2 =pd.read_csv('Movies_clean.csv')
df2.drop(df2.columns[0], axis=1, inplace =True)
#df3.replace('', np.NaN) # replace empty with nan
# subset to only USA

by_Language =df2.groupby(['primary_language']).size() # 12659 English
by_Country=df2.groupby(['country']).size() # 9006 US movies

df3 = df2[(df2.country =='USA')]


# create a indicator of type of currency

# opening_weekend_revenue




### Clean and Convert revenues to float from string
# gross_revenue 
df3.gross_revenue = df3.gross_revenue.str.replace(',', '') # remove commas
df3.gross_revenue = df3.gross_revenue.astype(np.float64)
    
#  opening_weekend_revenue 

# keep £ rows, create an indicator for dollar versus pound  
  
Indicator =(df3.opening_weekend_revenue.str.contains('\(UK', regex=True, na=False).values).astype('int')
df3['open_week_rev_currency'] = pd.Series(['pound'* x + 'dollar'*(1-x) for x in Indicator], index = df3.index)  


df3 = df3[-df3.opening_weekend_revenue.str.contains('\(Mexico', regex=True, na=False)]  # remove movies with Mexico, 3 instances, no budget, low revenue
df3 = df3[-df3.opening_weekend_revenue.str.contains('\(France', regex=True, na=False)]   ## France # removed
    
df3.opening_weekend_revenue = df3.opening_weekend_revenue.str.replace(",|£|\(.*", "")    
#df3.opening_weekend_revenue = df3.opening_weekend_revenue.str.replace("£", "")
#df3.opening_weekend_revenue = df3.opening_weekend_revenue.str.replace("\(UK", "")
#df3.opening_weekend_revenue = df3.opening_weekend_revenue.str.replace("\(Australia", "")

## just remove strings starting with ( and then remove space 
#df3.opening_weekend_revenue = df3.opening_weekend_revenue.str.replace("\(.*", "")
df3.opening_weekend_revenue = [str(x).strip() for x in df3.opening_weekend_revenue.values]

# convert to float
df3.opening_weekend_revenue = df3.opening_weekend_revenue.astype(np.float64)



# budget 
df3.budget = df3.budget.str.replace(',', '') 
df3 = df3[-df3.budget.str.contains('PYG|£|CAD|SEK|€|SGD', regex=True, na=False)]  
df3.budget = df3.budget.astype(np.float64)    
 
#df3[df3.budget.str.contains('SGD', regex=True, na=False)]
 
 # make a copy
df3.to_csv('Movies_cleaner.csv')
 
# convert date to datetime format
 
# openingweekend
df3.opening_weekend_date = df3.opening_weekend_date.str.replace(' ', '') 
# replace mising values with NA
df3.opening_weekend_date = df3.opening_weekend_date.replace(r'\s+', np.nan, regex=True).replace('',np.nan)
#df3.opening_weekend_date = df3.opening_weekend_date.str.replace('30September2016', '30 September 2016') 
for i in df3.opening_weekend_date.index:
    x=df3.loc[i,'opening_weekend_date']
    if len(str(x))>3:
        df3.loc[i, 'Date_weekend'] = datetime.strptime(str(x), '%d%B%Y')
    else:
        df3.loc[i, 'Date_weekend'] = None

# release_date

df3.release_date = df3.release_date.str.replace(' ', '')

for i in df3.release_date.index:
    x=df3.loc[i,'release_date']
    if len(str(x))>3:
        df3.loc[i, 'Date_released'] = datetime.strptime(str(x), '%d%B%Y')
    else:
        df3.loc[i, 'Date_released'] = None        
        
#gross_revenue_date        

df3.gross_revenue_date = df3.gross_revenue_date.str.replace(' ', '')        
for i in df3.gross_revenue_date.index:
    x=df3.loc[i,'gross_revenue_date']
    if len(str(x))>3:
        df3.loc[i, 'Date_GrossRev'] = datetime.strptime(str(x), '%d%B%Y')
    else:
        df3.loc[i, 'Date_GrossRev'] = None    


#df3[df3.opening_weekend_date.str.contains('14October2016', regex=True, na=False)]


df3.to_csv('Movies_cleaner2.csv')

