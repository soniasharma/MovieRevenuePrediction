# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:37:30 2016

@author: sonia
"""

from lxml import html
import requests
import pandas as pd
import time 
import re
from datetime import datetime

all_movies_df = pd.read_csv('Data/movies_only_list.csv')
links = all_movies_df['movie_page_link']


movies_data = pd.DataFrame() # data frame whih will be appended at each iteration
   #url = 'http://www.imdb.com/title/tt2446980/?ref_=adv_li_tt' # movie joy

start = time.time()
counter = 0
for index, value in links.iteritems():
    if index >= 18609:
        url = 'http://www.imdb.com' + value
    
        page = requests.get(url)
        tree = html.fromstring(page.content)
        
        s = ";" # separtor for joining strings of features with multiple elements
        
        title = tree.xpath('//div[@class="mini-article"]//div[@id="ratingWidget"]//p//strong/text()')
        release_date = tree.xpath('//div[@id="title-overview-widget"]//a[@title="See more release dates"]/text()')
        if len(release_date)==0:
            release_date = ""
        else:
            release_date=release_date[0]
        release_date=(re.sub('\(.*\)\n', '', release_date)).strip() # remove country attribute
        length = len(str.split(release_date, ' '))
        if not bool(re.search('TV|2017', release_date)) and (length == 3) and (len(title)>0): 
            if datetime.strptime(release_date, '%d %B %Y') > datetime.now(): # if movie not released, stop scraping 
               print('movie not released yet')
            else:
            
                user_rating =tree.xpath('//div[@class="mini-article"]//div[@id="ratingWidget"]//span[@class="rating"]/text()') # out of 10
                if len(user_rating)==0:
                    user_rating = " " 
                plot_summary=tree.xpath('//div[@class="plot_summary "]//div[@class="summary_text"]//text()')
                plot_summary=s.join(plot_summary)
                if len(plot_summary)==0:
                    plot_summary=" "            
                writers=tree.xpath('//div[@class="plot_summary "]//div[@class="credit_summary_item"][h4[@class="inline"]="Writers:"]//a//span//text()')
                writers = s.join(writers)
                if len(writers)==0:
                    writers = " "
                director=tree.xpath('//div[@class="plot_summary "]//div[@class="credit_summary_item"][h4[@class="inline"]="Director:"]//a//span//text()')
                director = s.join(director)
                if len(director)==0:
                    director = " "
                actors=tree.xpath('//div[@class="plot_summary "]//div[@class="credit_summary_item"][h4[@class="inline"]="Stars:"]//a//span//text()') #mutiple values
                actors = s.join(actors)
                if len(actors)== 0:
                    actors =" "
                meta_score=tree.xpath('//div[@class="metacriticScore score_mixed titleReviewBarSubItem"]//span//text()')
                if len(meta_score)==0:
                    meta_score = " "
                #popularity=tree.xpath('//div[@class="titleReviewBarItem"]//div[@class="titleOverviewSprite popularityTrendUp"]//text()')
                #popularity=tree.xpath('//div[@class="titleReviewBarItem"]//div[@class="titleReviewBarSubItem"][div = "\n Popularity \n"]//span[@class="subText"]/text()')
                #popularity=tree.xpath('div[@class="titleReviewBarSubItem"][div = "\n Popularity \n"]//text()')
                
                
                plot_keywords=tree.xpath('//div[@id="titleStoryLine"]//div[@class="see-more inline canwrap"][h4[@class="inline"]="Plot Keywords:"]//a//span//text()') # multiple values
                plot_keywords = s.join(plot_keywords)
                if len(plot_keywords)==0:
                    plot_keywords=" "
                genres=tree.xpath('//div[@id="titleStoryLine"]//div[@class="see-more inline canwrap"][h4[@class="inline"]="Genres:"]//a//text()') # multiple values
                genres = s.join(genres)
                if len(genres)==0:
                    genres =" "
                tag_lines=tree.xpath('//div[@id="titleStoryLine"]//div[@class="txt-block"][h4[@class="inline"]="Taglines:"]//text()')
                if len(tag_lines) <2 :
                    tag_lines = " "
                else:
                    tag_lines =tag_lines[2]
                     
                #tag_lines=s.join(tag_lines)
                #MP_rating=tree.xpath('//div[@class="txt-block"][h4="Motion Picture Rating"]//span[@itemprop="contentRating"]\text()')
                country = tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Country:"]//a//text()')
                if len(country)==0:
                    country = " "
                else:
                    country=country[0]
                primary_language = tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Language:"]//a//text()') # multiple languages
                if len(primary_language)==0:
                    primary_language =""
                else:
                    primary_language=primary_language[0]   
                #release_date = tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Release Date:"]//text()')[2] # check if the index works for other pages
                budget = tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Budget:"]//text()')
                if len(budget) < 2:
                    budget = " "
                else:
                    budget =budget[2]
                opening_weekend = tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Opening Weekend:"]//text()')
                if len(opening_weekend) > 2:
                    opening_weekend_revenue = opening_weekend[2]
                    opening_weekend_date = opening_weekend[3]
                else:
                    opening_weekend_revenue = ' '
                    opening_weekend_date = ' '
                gross =tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Gross:"]//text()')
                if len(gross) > 4:
                    gross_revenue = gross[2]
                    gross_revenue_date = gross[5]
                else:
                    gross_revenue = ' '
                    gross_revenue_date = ' '
                    
                production_company=tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Production Co:"]//span[@class="itemprop"]//text()') # multiple values
                production_company = s.join(production_company)
                if len(production_company)==0:
                    production_company= " "
                runtime=tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Runtime:"]//time/text()')
                if len(runtime)==0:
                    runtime=" "
                else:
                    runtime=runtime[0]
                sound_mix=tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Sound Mix:"]//a/text()')
                sound_mix = s.join(sound_mix)
                if len(sound_mix)==0:
                    sound_mix=" "
                color=tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Color:"]//a/text()')
                color = s.join(color)
                if len(color)==0:
                    color=" "
                #aspect_ratio=tree.xpath('//div[@id="titleDetails"]//div[@class="txt-block"][h4[@class="inline"]="Aspect Ratio:"]//text()')[2]
                
                my_df = pd.DataFrame({'title':title, 'user_rating': user_rating, 'plot_summary' : plot_summary, 'writers': writers, 'director':director, 'actors' : actors, 'meta_score' : meta_score, 'plot_keywords': plot_keywords, 'genres': genres, 'tag_lines':tag_lines, 'country':country, 'primary_language':primary_language, 'production_company':production_company, 'runtime':runtime, 'sound_mix': sound_mix, 'color':color, 'release_date':release_date, 'budget':budget, 'opening_weekend_revenue':opening_weekend_revenue, 'opening_weekend_date':opening_weekend_date, 'gross_revenue_date':gross_revenue_date, 'gross_revenue':gross_revenue })
                
                movies_data = pd.concat([movies_data, my_df]) # append data frame
                
                if counter == 0:
                    movies_data.to_csv('movies_data.csv', mode = 'a', header =True)
                elif  counter % 10 == 0:
                    movies_data.to_csv('movies_data.csv', mode = 'a', header =False)
                    print("Scarped", index, "movies" )
                    print("total time taken for far: ", time.time() - start)
                    #break
                print('read', index)
                counter = counter + 1
        
        
