#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from collections import Counter
from datetime import datetime
import string
import re
print(os.listdir("input"))


# In[ ]:





# In[2]:


data = pd.read_csv('data.csv')
data.sample(5)


# In[3]:


len(data)


# # Предобработка датасета

# In[4]:


def custom_count(df,col,sep): #эта функция нужна для того, чтобы учесть разделитель и будет использоваться далее для подсчета количества
    items=[]
    for item in df[col]:
        items+=item.split(sep)
    return Counter(items).most_common()
def season(str):
    dt = datetime.strptime(str,'%m/%d/%Y')
    if dt.month in [12,1,2,]:
        return 'winter'
    elif dt.month in [3,4,5]:
        return 'spring'
    elif dt.month in [6,7,8]:
        return 'summer'
    else: return 'autumn'


# In[177]:


answer_ls = [] # создадим список с ответами. сюда будем добавлять ответы по мере прохождения теста
# сюда можем вписать создание новых колонок в датасете
data['profit'] = data.apply(lambda x: x['revenue'] - x['budget'], axis = 1) # значения прибыли
data['month'] = data.apply(lambda x: datetime.strptime(x['release_date'], '%m/%d/%Y').month, axis = 1 ) # отдельно месяца
data['season'] = data.apply(lambda x: season(x['release_date']), axis = 1 ) # отдельно сезоны
data['words'] = data.apply(lambda x: len(x['original_title'].split(' ')), axis = 1)
data['symbols'] = data.apply(lambda x: len(x['original_title'].replace(' ','')), axis = 1)
data['productivity'] = data.apply(lambda x: 1 if x['profit'] > x['budget'] else 0, axis = 1)


# In[ ]:





# In[63]:


actors=[]
for cast in data.cast:
     actors+=cast.split('|')
actors_list=list(set(actors))
actors=pd.Series(index = actors_list) #cписок всех уникальных актеров

companies=[]
for company in data.production_companies:
     companies+=company.split('|')
companies=pd.Series(index = list(set(companies))) # cписок всех уникальных студий

pattern=re.compile('[0-9a-z.\!?_/#№%&()\-\+=\'\"~`$^]*')
unique_words=[]
for words in data.original_title:
     unique_words+=pattern.findall(words.lower())
unique_words=pd.Series(index = list(set(unique_words)))
unique_words


# In[190]:


for i in actors.index:
    actors.loc[i]=data[data.cast.str.contains(i)].profit.sum()


# In[193]:


for j in companies.index:
    companies.loc[i]=data[data.production_companies.str.contains(i)].profit.sum()


# # 1. У какого фильма из списка самый большой бюджет?
# Варианты ответов:
# 1. The Dark Knight Rises (tt1345836)
# 2. Spider-Man 3 (tt0413300)
# 3. Avengers: Age of Ultron (tt2395427)
# 4. The Warrior's Way	(tt1032751)
# 5. Pirates of the Caribbean: On Stranger Tides (tt1298650)

# In[7]:


data[data.budget == data.budget.max()]


# In[135]:


# тут вводим ваш ответ и добавлем в его список ответов (сейчас для примера стоит "1")
answer_ls.append(4)


# # 2. Какой из фильмов самый длительный (в минутах)
# 1. The Lord of the Rings: The Return of the King	(tt0167260)
# 2. Gods and Generals	(tt0279111)
# 3. King Kong	(tt0360717)
# 4. Pearl Harbor	(tt0213149)
# 5. Alexander	(tt0346491)

# In[39]:


data[data.runtime == data.runtime.max()]


# In[136]:


answer_ls.append(2)


# # 3. Какой из фильмов самый короткий (в минутах)
# Варианты ответов:
# 
# 1. Home on the Range	tt0299172
# 2. The Jungle Book 2	tt0283426
# 3. Winnie the Pooh	tt1449283
# 4. Corpse Bride	tt0121164
# 5. Hoodwinked!	tt0443536

# In[41]:


data[data.runtime == data.runtime.min()]


# In[137]:


answer_ls.append(3)


# # 4. Средняя длительность фильма?
# 
# Варианты ответов:
# 1. 115
# 2. 110
# 3. 105
# 4. 120
# 5. 100
# 

# In[43]:


data.runtime.mean()


# In[138]:


answer_ls.append(2)


# # 5. Средняя длительность фильма по медиане?
# Варианты ответов:
# 1. 106
# 2. 112
# 3. 101
# 4. 120
# 5. 115
# 
# 
# 

# In[45]:


data.runtime.median()


# In[139]:


answer_ls.append(1)


# # 6. Какой самый прибыльный фильм?
# Варианты ответов:
# 1. The Avengers	tt0848228
# 2. Minions	tt2293640
# 3. Star Wars: The Force Awakens	tt2488496
# 4. Furious 7	tt2820852
# 5. Avatar	tt0499549

# In[86]:


data[data.profit == data.profit.max()]['original_title']


# In[140]:


answer_ls.append(5)


# # 7. Какой фильм самый убыточный?
# Варианты ответов:
# 1. Supernova tt0134983
# 2. The Warrior's Way tt1032751
# 3. Flushed Away	tt0424095
# 4. The Adventures of Pluto Nash	tt0180052
# 5. The Lone Ranger	tt1210819

# In[85]:


data[data.profit == data.profit.min()]['original_title']


# In[141]:


answer_ls.append(2)


# # 8. Сколько всего фильмов в прибыли?
# Варианты ответов:
# 1. 1478
# 2. 1520
# 3. 1241
# 4. 1135
# 5. 1398
# 

# In[55]:


data_profitable = data[data.profit>0]
len(data_profitable)


# In[142]:


answer_ls.append(1)


# # 9. Самый прибыльный фильм в 2008 году?
# Варианты ответов:
# 1. Madagascar: Escape 2 Africa	tt0479952
# 2. Iron Man	tt0371746
# 3. Kung Fu Panda	tt0441773
# 4. The Dark Knight	tt0468569
# 5. Mamma Mia!	tt0795421

# In[84]:


data.query('release_year == 2008').sort_values(by='profit', ascending=False).iloc[0]['original_title']


# In[143]:


answer_ls.append(4)


# # 10. Самый убыточный фильм за период с 2012 по 2014 (включительно)?
# Варианты ответов:
# 1. Winter's Tale	tt1837709
# 2. Stolen	tt1656186
# 3. Broken City	tt1235522
# 4. Upside Down	tt1374992
# 5. The Lone Ranger	tt1210819
# 

# In[83]:


data.query('2015> release_year >2011').sort_values(by='profit', ascending=True).iloc[0]['original_title']


# In[144]:


answer_ls.append(5)


# # 11. Какого жанра фильмов больше всего?
# Варианты ответов:
# 1. Action
# 2. Adventure
# 3. Drama
# 4. Comedy
# 5. Thriller

# In[155]:


custom_count(data,'genres','|')


# In[145]:


answer_ls.append(3)


# # 12. Какого жанра среди прибыльных фильмов больше всего?
# Варианты ответов:
# 1. Drama
# 2. Comedy
# 3. Action
# 4. Thriller
# 5. Adventure

# In[160]:


custom_count(data_profitable,'genres','|')


# In[146]:


answer_ls.append(1)


# # 13. Кто из режиссеров снял больше всего фильмов?
# Варианты ответов:
# 1. Steven Spielberg
# 2. Ridley Scott 
# 3. Steven Soderbergh
# 4. Christopher Nolan
# 5. Clint Eastwood

# In[20]:


custom_count(data, 'director','|')


# In[147]:


answer_ls.append(3)


# # 14. Кто из режиссеров снял больше всего Прибыльных фильмов?
# Варианты ответов:
# 1. Steven Soderbergh
# 2. Clint Eastwood
# 3. Steven Spielberg
# 4. Ridley Scott
# 5. Christopher Nolan

# In[162]:


custom_count(data_profitable,'director','|')


# In[148]:


answer_ls.append(4)


# # 15. Кто из режиссеров принес больше всего прибыли?
# Варианты ответов:
# 1. Steven Spielberg
# 2. Christopher Nolan
# 3. David Yates
# 4. James Cameron
# 5. Peter Jackson
# 

# In[35]:


data.groupby(['director']).sum()['profit'].sort_values(ascending=False)


# In[149]:


answer_ls.append(5)


# # 16. Какой актер принес больше всего прибыли?
# Варианты ответов:
# 1. Emma Watson
# 2. Johnny Depp
# 3. Michelle Rodriguez
# 4. Orlando Bloom
# 5. Rupert Grint

# In[196]:


for i in actors.index:
    actors.loc[i]=data[data.cast.str.contains(i)].profit.sum()
actors.sort_values(ascending=False)


# In[150]:


answer_ls.append(1)


# # 17. Какой актер принес меньше всего прибыли в 2012 году?
# Варианты ответов:
# 1. Nicolas Cage
# 2. Danny Huston
# 3. Kirsten Dunst
# 4. Jim Sturgess
# 5. Sami Gayle

# In[198]:


for i in actors.index:
    actors.loc[i]=data[(data.release_year == 2012)&(data.cast.str.contains(i))].profit.sum()
actors.sort_values()


# In[151]:


answer_ls.append(3)


# # 18. Какой актер снялся в большем количестве высокобюджетных фильмов? (в фильмах где бюджет выше среднего по данной выборке)
# Варианты ответов:
# 1. Tom Cruise
# 2. Mark Wahlberg 
# 3. Matt Damon
# 4. Angelina Jolie
# 5. Adam Sandler

# In[165]:


custom_count(data[data.budget>data.budget.mean()],'cast','|')


# In[152]:


answer_ls.append(3)


# # 19. В фильмах какого жанра больше всего снимался Nicolas Cage?  
# Варианты ответа:
# 1. Drama
# 2. Action
# 3. Thriller
# 4. Adventure
# 5. Crime

# In[163]:


custom_count(data[data.cast.str.contains("Nicolas Cage")],'genres','|')
# genres = []
# for genre in data[data.cast.str.contains("Nicolas Cage", na=False)]['genres']:
#     genres+=genre.split('|')
# Counter(genres).most_common()[0]


# In[153]:


answer_ls.append(2)


# # 20. Какая студия сняла больше всего фильмов?
# Варианты ответа:
# 1. Universal Pictures (Universal)
# 2. Paramount Pictures
# 3. Columbia Pictures
# 4. Warner Bros
# 5. Twentieth Century Fox Film Corporation

# In[84]:


for c in companies.index:
    companies.loc[c]=len(data[data.production_companies.str.contains(c)])
companies.sort_values(ascending = False).head(1)


# In[154]:


answer_ls.append(1)


# # 21. Какая студия сняла больше всего фильмов в 2015 году?
# Варианты ответа:
# 1. Universal Pictures
# 2. Paramount Pictures
# 3. Columbia Pictures
# 4. Warner Bros
# 5. Twentieth Century Fox Film Corporation

# In[83]:


for c in companies.index:
    companies.loc[c]=len(data[(data.release_year == 2015) & (data.production_companies.str.contains(c))])
companies.sort_values(ascending = False).head(1)


# In[155]:


answer_ls.append(4)


# # 22. Какая студия заработала больше всего денег в жанре комедий за все время?
# Варианты ответа:
# 1. Warner Bros
# 2. Universal Pictures (Universal)
# 3. Columbia Pictures
# 4. Paramount Pictures
# 5. Walt Disney

# In[82]:


g_filter = 'Comedy'
data_filtered = data[data.genres.str.contains(g_filter)]
for i in companies.index:
    companies.loc[i]=data_filtered[data_filtered.production_companies.str.contains(i)].profit.sum()
companies.sort_values(ascending = False).head(1)


# In[156]:


answer_ls.append(2)


# # 23. Какая студия заработала больше всего денег в 2012 году?
# Варианты ответа:
# 1. Universal Pictures (Universal)
# 2. Warner Bros
# 3. Columbia Pictures
# 4. Paramount Pictures
# 5. Lucasfilm

# In[80]:


for i in companies.index:
    companies.loc[i]=data[(data.release_year == 2012)&(data.production_companies.str.contains(i))].profit.sum()
companies.sort_values(ascending = False).head(1)


# In[157]:


answer_ls.append(3)


# # 24. Самый убыточный фильм от Paramount Pictures
# Варианты ответа:
# 
# 1. K-19: The Widowmaker tt0267626
# 2. Next tt0435705
# 3. Twisted tt0315297
# 4. The Love Guru tt0811138
# 5. The Fighter tt0964517

# In[189]:


data[data.production_companies.str.contains('Paramount')].sort_values('profit')


# In[158]:


answer_ls.append(1)


# # 25. Какой Самый прибыльный год (заработали больше всего)?
# Варианты ответа:
# 1. 2014
# 2. 2008
# 3. 2012
# 4. 2002
# 5. 2015

# In[184]:


data.groupby(by = ['release_year']).sum().sort_values(by = ['profit'], ascending = False)


# In[159]:


answer_ls.append(5)


# # 26. Какой Самый прибыльный год для студии Warner Bros?
# Варианты ответа:
# 1. 2014
# 2. 2008
# 3. 2012
# 4. 2010
# 5. 2015

# In[187]:


data[data.production_companies.str.contains("Warner")].groupby(by = ['release_year']).sum().sort_values(by = ['profit'], ascending = False)


# In[160]:


answer_ls.append(1)


# # 27. В каком месяце за все годы суммарно вышло больше всего фильмов?
# Варианты ответа:
# 1. Январь
# 2. Июнь
# 3. Декабрь
# 4. Сентябрь
# 5. Май

# In[71]:


Counter(data.month).most_common()


# In[161]:


answer_ls.append(4)


# # 28. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)
# Варианты ответа:
# 1. 345
# 2. 450
# 3. 478
# 4. 523
# 5. 381

# In[70]:


Counter(data.season).most_common()


# In[162]:


answer_ls.append(2)


# # 29. Какой режисер выпускает (суммарно по годам) больше всего фильмов зимой?
# Варианты ответов:
# 1. Steven Soderbergh
# 2. Christopher Nolan
# 3. Clint Eastwood
# 4. Ridley Scott
# 5. Peter Jackson

# In[53]:


custom_count(data[data.season=='winter'],'director','|')


# In[163]:


answer_ls.append(5)


# # 30. Какой месяц чаще всего по годам самый прибыльный?
# Варианты ответа:
# 1. Январь
# 2. Июнь
# 3. Декабрь
# 4. Сентябрь
# 5. Май

# In[165]:


def best_month(df):
    lst=[]
    for i in range(2000,2016):
        lst.append(df[df.release_year == i].groupby(['month']).sum().sort_values(by = ['profit'],ascending = False).index[0])
    return Counter(lst).most_common()
best_month(data)


# In[166]:


answer_ls.append(2)


# # 31. Названия фильмов какой студии в среднем самые длинные по количеству символов?
# Варианты ответа:
# 1. Universal Pictures (Universal)
# 2. Warner Bros
# 3. Jim Henson Company, The
# 4. Paramount Pictures
# 5. Four By Two Productions

# In[102]:


for i in companies.index:
    companies.loc[i]=data[data.production_companies.str.contains(i)].symbols.mean()
companies.sort_values(ascending = False).head(1)


# In[167]:


answer_ls.append(5)


# # 32. Названия фильмов какой студии в среднем самые длинные по количеству слов?
# Варианты ответа:
# 1. Universal Pictures (Universal)
# 2. Warner Bros
# 3. Jim Henson Company, The
# 4. Paramount Pictures
# 5. Four By Two Productions

# In[103]:


for i in companies.index:
    companies.loc[i]=data[data.production_companies.str.contains(i)].words.mean()
companies.sort_values(ascending = False).head(1)


# In[168]:


answer_ls.append(5)


# # 33. Сколько разных слов используется в названиях фильмов?(без учета регистра)
# Варианты ответа:
# 1. 6540
# 2. 1002
# 3. 2461
# 4. 28304
# 5. 3432

# In[120]:


len(unique_words) #грубо, но с небольшой переменой фильтров (с цифрами, без цифр, с/без знаков препинания) попадает в порядок


# In[169]:


answer_ls.append(3)


# # 34. Какие фильмы входят в 1 процент лучших по рейтингу?
# Варианты ответа:
# 1. Inside Out, Gone Girl, 12 Years a Slave
# 2. BloodRayne, The Adventures of Rocky & Bullwinkle
# 3. The Lord of the Rings: The Return of the King
# 4. 300, Lucky Number Slevin

# In[119]:


#len(data[data.vote_average > data.vote_average.median()])*0.01 
#1% от всей выборки - это 19 штук до рейтинга 7.8 включительно, 1% от "выше среднего" это до рейтинга 7.9 включительно и примерно 9 штук, у gone girl тот же рейтинг 7.9, что и у девятого элемента в срезе, так что можно считать, что входит 
data.sort_values(by = ['vote_average'], ascending = False).head(19)


# In[170]:


answer_ls.append(1)


# # 35. Какие актеры чаще всего снимаются в одном фильме вместе
# Варианты ответа:
# 1. Johnny Depp & Helena Bonham Carter
# 2. Hugh Jackman & Ian McKellen
# 3. Vin Diesel & Paul Walker
# 4. Adam Sandler & Kevin James
# 5. Daniel Radcliffe & Rupert Grint

# In[133]:


def in_movie(df, name1,name2):
    p=0
    for actor in df.cast:
        if (name1 in actor) & (name2 in actor) == True:
            p+=1
    return p



# In[171]:


answer_ls.append(5)


# # 36. У какого из режиссеров выше вероятность выпустить фильм в прибыли? (5 баллов)101
# Варианты ответа:
# 1. Quentin Tarantino
# 2. Steven Soderbergh
# 3. Robert Rodriguez
# 4. Christopher Nolan
# 5. Clint Eastwood

# In[200]:


productive = data.groupby(['director']).mean().sort_values(by = ['popularity','productivity','vote_average'], ascending = False).head(20)
productive


# In[ ]:





# In[172]:


answer_ls.append(4)


# # Submission

# In[173]:


len(answer_ls)


# In[174]:


pd.DataFrame({'Id':range(1,len(answer_ls)+1), 'Answer':answer_ls}, columns=['Id', 'Answer'])


# In[ ]:




