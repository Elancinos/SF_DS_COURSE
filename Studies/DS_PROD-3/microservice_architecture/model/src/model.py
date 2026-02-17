#Импорты
import pika
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import json

try:
    #Чтение файла с моделью
    with open('myfile.pkl', 'rb') as pkl_file:
        regressor = pickle.load(pkl_file)
        
    #Подключение к серверу
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    #Рабочая очередь:
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')

    #Функция-обработчик, выводит на экран сообщение из очереди
    def callback(ch, method, properties, body):
        print(f'Получен вектор признаков {body}!')
        features = json.loads(body)
        shaped_features = np.array(features).reshape(1, -1)
        y_pred = regressor.predict(shaped_features)
        channel.basic_publish(exchange='', routing_key='y_pred', body=json.dumps(y_pred[0]))
        print(f'Предсказание {y_pred[0]} добавлено в очередь!')

    #Извлекаем сообщение из очереди features
    #on_message_callback показывает, какую функцию вызывать при получении сообщения
    channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    #Запуск режима ожидания сообщений
    channel.start_consuming()

except:
    print('Произошла одна или несколько ошибок, подключение к очереди невозможно!')