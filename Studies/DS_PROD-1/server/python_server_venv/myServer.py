from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import sklearn
import datetime

app = Flask(__name__)

@app.route('/hello')
def hello_func():
    name = request.args.get('name')
    return f'hello, {name}!'

@app.route('/')
def index():
    return 'Test message. The server is running'

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
    
#Задание 7.6
@app.route('/predict', methods=['POST'])
def predict():
    
    #Десериализуем модель
    with open('/models/model.pkl', 'rb') as pkl_model:
        loaded_model = pickle.load(pkl_model)
    
    #Небольшая предобработка и получение предсказания
    features = request.json
    features = np.array(features).reshape(1, 4)
    prediction = loaded_model.predict(features)
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run('localhost', 5000)
