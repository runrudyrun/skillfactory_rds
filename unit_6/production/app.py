import streamlit as st
import numpy as np
import pandas as pd
import lightfm as lf
import nmslib
import pickle
import scipy.sparse as sparse

def nearest_item(itemid, index, n=10):
    """Функция для поиска ближайших соседей, возвращает построенный индекс"""
    nn = index.knnQuery(item_embeddings[itemid], k=n)
    return nn

def get_names(index):
    """
    input - idx of items
    Функция для возвращения имени продукта
    return - list of names
    """
    names = []
    for idx in index:
        names.append('Item name:  {} '.format(
            name_mapper[idx]) + '  Main_cat: {}'.format(category_mapper[idx]))
    return names

def read_files(folder_name='data'):
    """
    Функция для чтения файлов + преобразование к  нижнему регистру
    """
    data = pd.read_excel(folder_name+'/data.xlsx')

    return data

def make_mappers():
    """
    Функция для создания отображения id в title
    """
    name_mapper = dict(zip(data.itemid, data.title))
    category_mapper = dict(zip(data.itemid, data.main_cat))

    return name_mapper, category_mapper

def load_embeddings():
    """
    Функция для загрузки векторных представлений
    """
    with open('./data/item_emb.pkl', 'rb') as f:
        item_embeddings = pickle.load(f)
    
    with open('./data/user_emb.pkl', 'rb') as f:
        user_embeddings = pickle.load(f)

    # Тут мы используем nmslib, чтобы создать наш быстрый knn
    nms_idx_i = nmslib.init(method='hnsw', space='cosinesimil')
    nms_idx_i.addDataPointBatch(item_embeddings)
    nms_idx_i.createIndex(print_progress=True)
    nms_idx_u = nmslib.init(method='hnsw', space='cosinesimil')
    nms_idx_u.addDataPointBatch(user_embeddings)
    nms_idx_u.createIndex(print_progress=True)
    return item_embeddings, nms_idx_i

#Загружаем данные
data  = read_files(folder_name='data') 
name_mapper, category_mapper = make_mappers()
item_embeddings, nms_idx_i= load_embeddings()

#Форма для ввода текста
title = st.text_input('Item Name', '')
title = title.lower()

#Наш поиск по айтемам
output = data[data.title.str.contains(title) > 0]

#Выбор айтема из списка
option = st.selectbox('Which item?', output['title'].values)

#Выводим айтем
'You selected: ', option

#Ищем рекомендации
val_index = output[output['title'].values == option].itemid
index_i = nearest_item(val_index, nms_idx_i, 5)

#Выводим рекомендации к ней
'What also you can by: '
st.write('', get_names(index_i[0])[1:])