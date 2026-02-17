#Базовый образ
FROM tiangolo/uwsgi-nginx-flask:python3.9

#Копируем приложение с сервером в корень контейнера
COPY ./app ./
#Копируем requirements в корень контейнера
COPY ./requirements.txt ./
#Копируем файл с настройками uwsgi в корень контейнера
COPY ./uwsgi.ini ./

#Запускаем установку необходимых библиотек
RUN pip install -r requirements.txt