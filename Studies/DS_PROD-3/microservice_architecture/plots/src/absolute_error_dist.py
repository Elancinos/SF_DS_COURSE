import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

while True:
    try:
        metric_log = pd.read_csv('./logs/metric_log.csv')
        fig = plt.figure(figsize=(12,6))
        sns.histplot(data=metric_log['absolute_error'], kde=True)
        plt.title('Распределение метрики абсолютных ошибок во времени')
        plt.savefig('./logs/error_dist.png')
        print('Файл с графиком распределения ошибок успешно сохранен!')
        
    except Exception as error:
        print('Ошибка визуализации!')
        print('Детали:', error)
        print(traceback.format_exc())