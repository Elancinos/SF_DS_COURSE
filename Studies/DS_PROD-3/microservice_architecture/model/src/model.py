#Импорты
import pika
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import json
import traceback

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
        message_in = json.loads(body)
        message_in_id = message_in['id']
        features = message_in['body']
        shaped_features = np.array(features).reshape(1, -1)
        y_pred = regressor.predict(shaped_features)[0]
        message_out = {'id': message_in_id, 'body': y_pred}
        channel.basic_publish(exchange='', routing_key='y_pred', body=json.dumps(message_out))
        print(f'Предсказание {message_out} добавлено в очередь!')

    #Извлекаем сообщение из очереди features
    #on_message_callback показывает, какую функцию вызывать при получении сообщения
    channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    #Запуск режима ожидания сообщений
    channel.start_consuming()

except Exception as error:
    print('Произошла одна или несколько ошибок, подключение к очереди невозможно!')
    print('Детали:', error)
    print(traceback.format_exc())