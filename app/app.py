from os import set_handle_inheritable
from flask import Flask, render_template, url_for, request, Response
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import matplotlib.patches as mpatches
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import plotly.express as px
import json


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


def cleanup(dataframe, country):
    df = dataframe.transpose()
    df = df.iloc[1:, :]
    df.columns = [country]
    df.index= pd.to_datetime(df.index)
    return df


@app.route('/result', methods=['GET', 'POST'])
def handle_data():
    country = request.form.get('column')
    country2 = request.form.get('c2')
    start_year = request.form.get('start_year')
    end_year = request.form.get('end_year')
    
    yearsentered = [start_year, end_year]
    yearsentered.sort()
    year1 = yearsentered[0]
    year2 = yearsentered[1]

    df = pd.read_csv("data/populationbycountry19802010millions.csv")

    df1 = df[df['Unnamed: 0'] == country]
    df2 = df[df['Unnamed: 0'] == country2]
    df1 = cleanup(df1, country)
    df2 = cleanup(df2, country2)
    df = pd.concat([df1, df2], axis=1)
    start_year = pd.to_datetime(year1)
    end_year = pd.to_datetime(year2)

    df = df[start_year:end_year]
    cols = df.columns
    df = df[cols].apply(pd.to_numeric, errors='coerce')
    df = df.pct_change()
   # df.apply(lambda row: row.fillna(row.mean()), axis=1)
    df.fillna(0, inplace=True)

    #df.at['1980-01-01', ] = 10
    fig = Figure()
    print(df)

    fig = px.line(df, x=df.index, y=df.columns, markers=True, title="Comparison of the populution changes")
        
    fig.update_layout(yaxis_tickformat = '.2%')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #graphJSON.append(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)) 

    return render_template('result.html', graphJSON=graphJSON)

@app.route('/', methods=['GET'])
def index():

    img = io.BytesIO()
    df = pd.read_csv("data/populationbycountry19802010millions.csv")
    df.dropna(inplace = True)
    df = df.sort_values(by=['Unnamed: 0'])
    print(df)
    columnheaders = df['Unnamed: 0']
    years = list(df.drop(['Unnamed: 0'], axis=1).columns.values)


    return render_template('index.html', columnheaders=columnheaders, years=years)

    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


    