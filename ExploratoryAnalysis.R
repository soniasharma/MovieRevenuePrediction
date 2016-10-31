library(ggplot2)
library(magrittr)
library(stringr)
library(dplyr)
library(reshape2)
library(lubridate)
library(scales)
library(tidyr)
library(cowplot)

df =read.csv('Movies_cleaner2.csv')

my_df = subset.data.frame(df, select =c(title, Date_released, budget, opening_weekend_revenue, gross_revenue))

my_df = na.omit(my_df) # drop na values

# convert release date to date/time class
my_df$Date_released = my_df$Date_released %>%
  strptime(format="%Y-%m-%d") %>%
  as.POSIXct()

# Analyze movies budget and revenue
grouped = my_df %>%
  group_by(Date_released) %>%
  summarize(Budget=mean(budget),
            First_weekend_revenue =mean(opening_weekend_revenue),
            Gross_revenue=mean(gross_revenue),
            count = n())

subgroup = grouped %>%
  filter(Date_released > '2015-01-01') 

melted = melt(grouped, id.vars=c(1,5))
melted$year = as.factor(year(melted$Date_released))
colnames(melted)[3] = 'Category'



# plot all revenue and expenses for all years, averaged over day

ggplot(melted, aes(Date_released, value)) +
  geom_point(aes(size = count, color=Category), alpha = .5) +
  facet_grid(.~year) +
  scale_size_area() +
  #geom_jitter(width = 1)+
  scale_y_continuous(labels=comma) +
  xlab("Release Year")+ylab('Amount ($)') + ggtitle('Movies average expenditure and revenues') +
  theme(axis.text.x=element_blank(),
        axis.ticks.x=element_blank())


### Plot # 1

### Plot by day of the week
melted$week = as.factor(weekdays(melted$Date_released))
grpby_week = melted %>%
  group_by(week, Category) %>%
  summarize(value=mean(value),
            count = n()) 

levels(grpby_week$week) = c('Fri', 'Mon', 'Sat', 'Sun', 'Thurs', 'Tues', 'Wed')
g_week = ggplot(grpby_week, aes(x=week, y = value,fill=Category))+
  geom_bar(stat='identity')+ scale_y_continuous(labels=comma)+
  xlab('') + ylab('dollars') +
  theme(axis.text.x = element_text(angle = 90, hjust=1),
        axis.ticks.x=element_blank())


## Plot 
# bargraph of expenditure and revenue by month averaged over all 10 years
melted$month = as.factor(month(melted$Date_released))

grpby_month = melted %>%
  group_by(month, Category) %>%
  summarize(value=mean(value),
            count = n()) 

grpby_month <- transform(grpby_month, month = as.factor(month.abb[month]))
levels(grpby_month$month) = month.abb

g_month = ggplot(grpby_month, aes(x=month, y = value,fill=Category))+
  geom_bar(stat='identity')+ scale_y_continuous(labels=comma)+
  xlab('') + ylab('dollars') + ggtitle("Movies expenditure and revenues")+
  theme(axis.text.x = element_text(angle = 90, hjust=1),
        axis.ticks.x=element_blank())
  

# Plot 
# bargraph of expenditure and revenue by year averaged over all 10 years
grpby_yr = melted %>%
  group_by(year, Category) %>%
  summarize(value=mean(value),
            count = n()) %>%
  arrange(year)

g_year =ggplot(grpby_yr, aes(x=year, y = value,fill=Category))+
  geom_bar(stat='identity')+ scale_y_continuous(labels=comma)+
  xlab('') + ylab('dollars') + ggtitle("Average movies expenditure and revenues per year")


plot_grid(g_month, g_week, nrow=2, align = 'v')

## Plot 2
# Analyze movies by genres

#unstack genres
s <- strsplit(as.character(df$genres), split = ";")
genres_df =data.frame(title = rep(df$title, sapply(s, length)), genres = unlist(s), release_date = rep(df$release_date, sapply(s, length)), budget = rep(df$budget, sapply(s, length)), Weekend_revenue = rep(df$opening_weekend_revenue, sapply(s, length)), gross_revenue = rep(df$gross_revenue, sapply(s, length)))

gpby_genre = genres_df %>%
  group_by(genres) %>%
  summarise(First_weekend_revenue = mean(Weekend_revenue, na.rm = TRUE),
            Gross_revenue=mean(gross_revenue, na.rm = TRUE), 
            Budget=mean(budget, na.rm=TRUE))
  
genre_melted = melt(gpby_genre, id.vars=1, na.rm=T)  
colnames(genre_melted)[2] = 'Category'
  
ggplot(genre_melted, aes(x=genres, y=value, fill=Category)) +
  geom_bar(stat='identity')+ scale_y_continuous(labels=comma)+
  xlab('') + ylab('Amount in dollars') + ggtitle("Average movies expenditure and revenues by genres")+
  coord_flip() +
  theme(axis.text.x = element_text(angle = 90, hjust=1),
        axis.ticks.x=element_blank())
  
  
  
  

