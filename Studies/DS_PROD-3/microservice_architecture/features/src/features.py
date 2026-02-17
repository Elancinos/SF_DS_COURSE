import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
from time import sleep
from datetime import datetime

# #Фиксация сида для воспроизводимости
# np.random.seed(42)

#Бесконечный цикл и система try-except для отправки сообщения в очередь

while True:
    try:
        
        #Загружаем дата-сет о диабете
        X, y = load_diabetes(return_X_y=True)

        #Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)

        #Подключение к серверу на локальном хосте
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        
        #Фиксируем время - будет как message_id
        message_id = datetime.timestamp(datetime.now())

        #Создаём очередь из y_true
        channel.queue_declare(queue='y_true')
        message_y_true = {
            'id': message_id,
            'body': y[random_row]
        }
        #Публикация предварительно сериализованного сообщения
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
        print('Сообщение с правильным ответом отправлено в очередь!')

        #Создание очереди features
        channel.queue_declare(queue='features')
        message_features = {
            'id': message_id,
            'body': list(X[random_row])
        }
        #Публикация предварительно сериализованного сообщения
        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
        print('Сообщение с вектором признаков отправлено в очередь!')

        #Если нужно очистить очередь:
        # channel.queue_purge(queue='имяочереди')

        #Закрыть подключение
        connection.close()
        
        #Пауза на 10 секунд после итерации
        sleep(10)
        
    except:
        print('Произошла одна или несколько ошибок, подключение к очереди невозможно!')