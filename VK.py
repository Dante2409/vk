#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def find_best_sales(filepath):
    # Читаем данные из CSV файла
    df = pd.read_csv(filepath, sep='\t')
    
    # Конвертируем столбец с временными метками в формат datetime для удобства работы с датами
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Создаем новый столбец с периодами в формате год-месяц
    df['year_month'] = df['timestamp'].dt.to_period('M')
    
    # Определяем первый и последний месяц в наборе данных
    first_month = df['year_month'].min()
    last_month = df['year_month'].max()
    
    # Исключаем данные за первый и последний месяц из анализа
    full_months = df[~df['year_month'].isin([first_month, last_month])]
    # Фильтруем подтвержденные покупки
    confirmations = full_months[full_months['action'] == 'confirmation']
    
    # Для каждого пользователя находим первую покупку
    first_purchases = confirmations.groupby('userid').first().reset_index()
    # Вытаскиваем дату из временной метки
    first_purchases['date'] = first_purchases['timestamp'].dt.date
    
    # Группируем данные по месяцам, находим максимальную сумму покупок для каждого дня
    output = first_purchases.groupby('year_month')[['date', 'value']].max().reset_index()
    # Удаляем столбец 'year_month', так как он больше не нужен
    output.drop('year_month', axis=1, inplace=True)
    # Переименовываем столбец 'date' в 'timestamp' для соответствия формату вывода
    output.rename(columns={'date': 'timestamp'}, inplace=True)

    # Сохраняем результат в CSV файл
    return output.to_csv('output.csv', index=False, sep='\t')

