import numpy as np
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pickle

app = Flask(__name__)

data = pickle.load(open(r'C:\app\IBM-master\data.pkl', 'rb'))


def power1(Text1):
    A = Text1
    x = data.iloc[:, 2].values
    y = data.iloc[:, 1].values
    for i in range(0, len(y)):
        if y[i] < 0:
            y[i] = -1 * y[i]
    poly = PolynomialFeatures(degree=3, interaction_only=False)
    X_poly = poly.fit_transform(x.reshape(-1, 1))
    poly.fit(X_poly, y)
    lin = LinearRegression()
    lin.fit(X_poly, y)
    d = []
    f = []
    for i in range(0, len(x)):
        if x[i] > 12:
            d.append(int(x[i]))
            f.append(int(y[i]))
    d = np.array(d)
    f = np.array(f)
    d = d ** 3
    lin1 = LinearRegression()
    lin1.fit(d.reshape(-1, 1), f)
    s = np.array([A])
    if A < 12:
        if A < 3:
            output = 0
        else:
            y1 = lin.predict(poly.fit_transform(s.reshape(-1, 1)))[0]
            output = y1
    else:
        if A >= 17:
            output = 3400
        else:
            output = lin1.predict(s.reshape(-1, 1))[0]
    result = output
    return result


def energy1(Text1, Text2, Text3):
    A = Text1
    B = Text2
    C = Text3
    x = data.iloc[:, 2].values
    y = data.iloc[:, 1].values
    for i in range(0, len(y)):
        if y[i] < 0:
            y[i] = -1 * y[i]

    poly = PolynomialFeatures(degree=3, interaction_only=False)
    X_poly = poly.fit_transform(x.reshape(-1, 1))
    poly.fit(X_poly, y)
    lin = LinearRegression()
    lin.fit(X_poly, y)
    d = []
    f = []
    for i in range(0, len(x)):
        if x[i] > 12:
            d.append(int(x[i]))
            f.append(int(y[i]))
    d = np.array(d)
    f = np.array(f)
    d = d ** 3
    lin1 = LinearRegression()
    lin1.fit(d.reshape(-1, 1), f)
    ac1 = (B - A) / (10 * 60)
    ac2 = (C - B) / (10 * 60)
    if ac1 > 0:
        if ac2 > 0:
            ac = (ac1 + ac2) / 2
        else:
            ac = ac2
    else:
        if ac2 > 0:
            ac = ac2
        else:
            ac = (ac1 + ac2) / 2
    w = []
    for i in range(1, 14):
        w.append(C + (i * 60 * 10 * ac))
    power_array = []
    for i in range(0, 13):
        power_array.append(power1(w[i]))
    e = []
    for i in range(12):
        e.append((power_array[i] + power_array[i + 1]) / 2)
    y = []
    for i in range(12):
        y.append(e[i] / 6)
    t = np.array(y)
    L = np.sum(t)
    result1 = L / 2
    return result1


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/services.html')
def services():
    return render_template('services.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/energy.html')
def energy():
    return render_template('energy.html')


@app.route('/power.html')
def power():
    return render_template('power.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    print(int_features)

    prediction = energy1(int_features[0], int_features[1], int_features[2])

    output = prediction

    return render_template('energy.html', prediction_energy='Predicted energy is kWh {}'.format(output))


@app.route('/predict1', methods=['POST'])
def predict1():
    int_features = [float(x) for x in request.form.values()]
    print(int_features)

    prediction = power1(int_features[0])

    output = prediction

    return render_template('power.html', prediction_power='Predicted POwer is kW {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
