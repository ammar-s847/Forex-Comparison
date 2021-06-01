import io
import requests
from flask import Response
from flask import Flask, redirect, url_for, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# config.py file
from config import headers

app = Flask(__name__)

url = "https://alpha-vantage.p.rapidapi.com/query"

data = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        from_currency = request.form['from-currency']
        to_currency = request.form['to-currency']
        return redirect(url_for("compare", _from=from_currency, _to=to_currency))
    else:
        return render_template('index.html')

@app.route('/<_from>to<_to>')
def compare(_from, _to):
    querystring = {
        "function":"FX_DAILY", # for current stat: "CURRENCY_EXCHANGE_RATE"
        "from_symbol":_from,
        "to_symbol":_to,
        "datatype":"json",
        "outputsize":"compact"
        }

    content = str()
    _datetime = str()
    message = str()
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        json_response = response.json()
        _datetime = f"Last Refreshed: {json_response['Meta Data']['5. Last Refreshed']}, Timezone: {json_response['Meta Data']['6. Time Zone']}"
        for key in json_response["Time Series FX (Daily)"]:
            data.append(f"{key}: {json_response['Time Series FX (Daily)'][key]['4. close']}")
        content = f"1 {_from} is equal to {data[0][data[0].index(' '):]} {_to}"
        message = f"x-axis shows each day, where day 0 is 100 days ago ({data[len(data) - 1][:data[len(data) - 1].index(' ') - 1]}) and day 100 is the current day."
    except:
        content = "Error"

    return render_template("compare.html", _to=_to, _from=_from, content=content, _datetime=_datetime, message=message, data=data)

@app.route('/plot.png') # Use matplotlib savefig function instead
def plot_png():
    global data
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = list()
    for i in data:
        number = data[data.index(i)][data[data.index(i)].index(' '):]
        ys.append(float(number))
    ys = ys[0:100]
    axis.plot(xs[::-1], ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    data = []
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
	app.run(debug=True)