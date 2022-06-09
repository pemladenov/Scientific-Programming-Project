from os import set_handle_inheritable
from flask import Flask, render_template, url_for, request, Response
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import seaborn as sns
import plotly
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import plotly.express as px
import json
import math
import random

sns.set(color_codes=True)


app = Flask(__name__)

@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    no_of_balls = 25
    x = [random.triangular() for i in range(no_of_balls)]
    y = [random.gauss(0.5, 0.25) for i in range(no_of_balls)]
    colors = [random.randint(1, 4) for i in range(no_of_balls)]
    areas = [math.pi * random.randint(5, 15)**2 for i in range(no_of_balls)]
    # draw the plot
    plt.figure()
    plt.scatter(x, y, s=areas, c=colors, alpha=0.85)
    plt.axis([0.0, 1.0, 0.0, 1.0])
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template("randomplot.html", img_data=plot_url)

def result(self) -> str:
    img = io.BytesIO()

    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('result.html', graph=plot_url)


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
    df.fillna(0, inplace=True)

    fig = Figure()
    print(df)

    fig = px.line(df, x=df.index, y=df.columns, markers=True, title="Comparison of the populution changes")
        
    fig.update_layout(yaxis_tickformat = '.2%')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

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
    print (columnheaders)
    print (years)

    return render_template('index.html', columnheaders=columnheaders, years=years)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


    