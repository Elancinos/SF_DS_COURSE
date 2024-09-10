#импорт библиотек

import os
import logging

# Функция для создания лог-файла и записи в него информации

def get_logger(path, file):
    """ Функция для создания лог-файла и записи в него информации

    Args:
        path (string): Путь к директории
        file (string): Имя файла

    Returns:
        object: логгер
    """    
    
    #Проверяем, существует ли файл
    log_file = os.path.join(path, file)
    
    #Если файла нет, создаём его:
    if not os.path.isfile(log_file):
        open(log_file, 'w+').close()
        
    #Меняем формат логирования
    file_logging_format = '%(levelname)s: %(asctime)s: %(message)s'
    
    #Конфигурируем лог-файл
    logging.basicConfig(
        level=logging.INFO,
        format=file_logging_format
        )
    logger = logging.getLogger()
    
    #Создадим хэндлер для записи лога в файл и установим уровень логирования
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    #Создадим формат логирования, используя file_logging_format
    formatter = logging.Formatter(file_logging_format)
    handler.setFormatter(formatter)
    
    #Добавим хэндлер лог-файлу
    logger.addHandler(handler)
    
    return logger