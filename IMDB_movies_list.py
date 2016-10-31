# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:07:03 2016

@author: sonia
"""

from lxml import html
import requests
import pandas as pd
import time 
import sys

years_list = pd.read_csv('Data/imdb_years.csv')

## Extract list for each year and write to a csv file
for yr in range(2004, 2015):
    link_to_year_list =  years_list.loc[years_list['year'] == yr].link
    #link_to_list_2015 = years_list.loc[years_list['year'] == 2015].link
    page = requests.get(link_to_year_list.values[0]) 
    tree = html.fromstring(page.content)

    name = tree.xpath('//h3[@class="lister-item-header"]//a//text()') # parse movie name
    movie_link = tree.xpath('//h3[@class="lister-item-header"]//a/@href') # parse the link to movie page
    release_year = tree.xpath('//h3//span[@class="lister-item-year text-muted unbold"]//text()') # parse the year of release



    nextpage_path = tree.xpath('//a[@class="lister-page-next next-page"]/@href')[0] # parse the link to got to the next page
    nextpage = 'http://www.imdb.com/search/title' + nextpage_path
    print('page', 1,  'extracted')

    df = pd.DataFrame({'name': name, 'release_year': release_year, 'movie_page_link': movie_link})

    start = time.time()
    # repeat the above process for all pages, and extend the lists
    for i in range(48):
        page = requests.get(nextpage)
        tree = html.fromstring(page.content)
    
        next_name = tree.xpath('//h3[@class="lister-item-header"]//a//text()')
        next_movie_link = tree.xpath('//h3[@class="lister-item-header"]//a/@href')
        next_release_year = tree.xpath('//h3//span[@class="lister-item-year text-muted unbold"]//text()')
        next_array = [next_name, next_movie_link,  next_release_year]
    
        if (len(next_name)== len(next_release_year)) & (len(next_release_year)==len(next_movie_link)):
            next_df = pd.DataFrame({'name': next_name, 'release_year': next_release_year, 'movie_page_link': next_movie_link})
            df = pd.concat([df, next_df])
            print(i+2, 'data frames merged')
   
        if i < 197:
            nextpage_path = tree.xpath('//a[@class="lister-page-next next-page"]/@href')[0]
            nextpage = 'http://www.imdb.com/search/title' + nextpage_path
        else:
            break
        print('page', i+2, 'extracted')
    print("total time taken this loop: ", time.time() - start)    


    # write to a file
    file_name = 'imdb_list_' + str(yr) + '.csv'
    df.to_csv(file_name)
    print(yr, 'done!')
