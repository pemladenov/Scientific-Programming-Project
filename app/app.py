from flask import Flask, render_template, url_for, request
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import numpy as np
import seaborn as sns
import plotly

sns.set(color_codes=True)


app = Flask(__name__)

@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


def result(self) -> str:
    img = io.BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('result.html', graph=plot_url)


@app.route('/login', methods=['POST', 'GET'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Error Message Text'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/result', methods=['POST'])
def handle_data():
    img = io.BytesIO()
    city = request.form['city']
    year = request.form['year']
    df = pd.read_csv("data/avocado.csv")

    df = df.drop(['4046', 
              '4225', 
              '4770', 
              'Total Bags',
              'Small Bags',
              'Large Bags',
              'XLarge Bags'], axis=1)

    df['Date']= pd.to_datetime(df['Date'])

    df = df.drop(df[(df.Date.dt.year != year) & (df.Date.dt.month != 1)].index)
    df = df.drop(df[(df.type=="conventional")].index)
    df = df[(df.region==city)]

    fig, ax = plt.subplots(figsize=(8,5))
    plt.ticklabel_format(style='plain')
    ax.scatter(df['Date'], 
            df['AveragePrice'], 
            color="blue", 
            alpha=1.0)
    ax.set_xlabel('Date')
    ax.set_ylabel('AveragePrice')
    plt.savefig(img, format='png')
    img.seek(0)

    graph = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(graph)
    
## return render_template('result.html',graph=plt)


@app.route("/")
def index():
    return render_template('index.html')

    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


    