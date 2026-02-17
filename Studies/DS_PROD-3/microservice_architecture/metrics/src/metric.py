#Импорты
import pika
import json

try:
    #Подключаемся к серверу
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    #Функция для получения сообщения
    def callback(ch, method, properties, body):
        log_string = f'из очереди {method.routing_key} получено значение {json.loads(body)}'
        with open('./logs/labels_log.txt', 'a') as log:
            log.write(log_string+'\n')

    #объявление очередей
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    #Публикация сообщений о предсказаниях
    channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)

    #Запуск режима ожидания сообщений
    print('...Ожидание сообщений. Для выхода нажмите CTRL+C.')
    channel.start_consuming()
    
except:
    print('Произошла одна или несколько ошибок, подключение к очереди невозможно!')