#Импорты
import pika
import json
import csv
import traceback
import pandas as pd

#Подключаем таблицу с логами из файла
log_table = pd.read_csv('./logs/metric_log.csv')

try:
    #Подключаемся к серверу
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    #Функция для получения сообщения
    def callback(ch, method, properties, body):
        
        message_id = json.loads(body)['id']
        message_body = json.loads(body)['body']
        log_string = f'из очереди {method.routing_key} получено значение {message_body}'
        
        with open('./logs/labels_log.txt', 'a') as labels_log:
            labels_log.write(log_string+'\n')
            
        log_table.loc[message_id, method.routing_key] = message_body
        
        if not any(log_table.loc[message_id, ['y_pred', 'y_true']].isna()):
            y_pred = log_table.loc[message_id, 'y_pred']
            y_true = log_table.loc[message_id, 'y_true']
            absolute_error = abs(y_pred - y_true)
            log_table.loc[message_id, 'absolute_error'] = absolute_error
            
            with open('./logs/metric_log.csv', 'a') as metric_log:
                row = csv.writer(metric_log, delimiter=',')
                row.writerow([message_id, y_true, y_pred, absolute_error])
                
        else:
            print('Есть пропуски или данные не поступили, попытка пропущена!')
            
    #объявление очередей
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    #Достаём сообщения о предсказаниях
    channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)

    #Запуск режима ожидания сообщений
    print('...Ожидание сообщений. Для выхода нажмите CTRL+C.')
    channel.start_consuming()
    
except Exception as error:
    print('Произошла одна или несколько ошибок, подключение к очереди невозможно!')
    print('Детали:', error)
    print(traceback.format_exc())