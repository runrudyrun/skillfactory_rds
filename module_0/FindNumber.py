#!/usr/bin/env python
# coding: utf-8

# In[2]:


def game_core(number): #самый очевидный и простой способ - бинарный поиск
    count = 0
    predict = 50 #берем в качестве первого предположения среднее значение из интервала от 0 до 100
    max1 = 100 #верхняя граница
    min1 = 0 #нижняя граница
    while number != predict:
        count+=1
        if number > predict:
            min1 = predict #так как загаданное число больше, то предположение становится новой нижней границей поиска
            predict = (min1+max1) // 2  #снова берём среднее значение
        elif number < predict:
            max1 = predict #так как загаданное число меньше, то предположение становится новой верхней границей поиска
            predict = (min1+max1) // 2 #снова берём среднее значение
    return(count)


# In[ ]:


import numpy as np
def score_game(game_core_v1): #функция симулирующая игру угадай число
    '''Запускаем игру 1000 раз, чтоб узнать как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=(250))
    for number in random_array:
        count_ls.append(game_core_v1(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)
score_game (game_core)

