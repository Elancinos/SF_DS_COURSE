import numpy as np


def game_core_v3(number: int = 1) -> int:
    """Генерируем случайное число от 1 до 100 и сравниваем его с загаданным.
    Если не совпало, начинаем перебирать варианты по принципу бинарного поиска.
    Функция принимает загаданное число и возвращает число попыток.
    
    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    # Ваш код начинается здесь
    
    count = 0
    min_number = 1
    max_number = 101
    predict_v3 = np.random.randint(min_number, max_number)
    # Генерация числа от 1 до 100, в названии переменной версия алгоритма
    
    while predict_v3 != number:
        count += 1
        #Предсказанную переменную приводим к середине массива вариантов:
        predict_v3 = min_number + (max_number - min_number)//2
        if predict_v3 > number:
            max_number = predict_v3
        else:
            min_number = predict_v3
    
    # Ваш код заканчивается здесь

    return count


def score_game(random_predict) -> int:
    """За какое количество попыток в среднем из 1000 подходов угадывает наш алгоритм

    Args:
        random_predict ([type]): функция угадывания

    Returns:
        int: среднее количество попыток
    """

    count_ls = [] # список для сохранения количества попыток
    random_array = np.random.randint(1, 101, size=(10000)) # загадали список чисел

    for number in random_array:
        count_ls.append(random_predict(number))

    score = int(np.mean(count_ls)) # находим среднее количество попыток

    print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
    return(score)


#Запускаем программу
score_game(game_core_v3)