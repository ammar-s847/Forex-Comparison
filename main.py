import io
import requests
from flask import Response
from flask import Flask, redirect, url_for, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from config import headers

app = Flask(__name__)

url = "https://alpha-vantage.p.rapidapi.com/query"

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
    data = []
    _datetime = str()
    message = str()
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        json_response = response.json()
        _datetime = f"Last Refreshed: {json_response['Meta Data']['5. Last Refreshed']}, Timezone: {json_response['Meta Data']['6. Time Zone']}"
        for key in json_response["Time Series FX (Daily)"]:
            data.append(f"{key}: {json_response['Time Series FX (Daily)'][key]['4. close']}")
        content = ", ".join(data)
        message = f"1 {_from} is equal to {data[len(data) - 1][11:]} {_to}"
    except:
        content = "Error"

    return render_template("compare.html", _to=_to, _from=_from, content=content, _datetime=_datetime, message=message)

'''
@app.route('/plot.png')
def plot_png():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')'''

if __name__ == "__main__":
	app.run(debug=True)