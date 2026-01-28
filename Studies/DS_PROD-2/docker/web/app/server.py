from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import sklearn
import datetime

# загружаем модель из файла
with open('./models/model.pkl', 'rb') as pkl_file:
    model = pickle.load(pkl_file)

# создаём приложение
app = Flask(__name__)


@app.route('/time')
def current_time():
    now = {'time': datetime.datetime.now()}
    return 'time is:', now['time']


@app.route('/add', methods=['POST'])
def add():
    num = request.json.get('num')
    if num > 10:
        return 'too much', 400
    return jsonify({
        'result': num + 1
    })


@app.route('/')
def index():
    msg = "Тестовое сообщение. Сервер запущен!"
    return msg


@app.route('/predict', methods=['POST'])
def predict():    
    #Небольшая предобработка и получение предсказания
    features = request.json
    features = np.array(features).reshape(1, 4)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)