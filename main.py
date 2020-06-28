import io
import requests
from flask import Response
from flask import Flask, redirect, url_for, render_template
from config import headers

app = Flask(__name__)

url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {
    "function":"CURRENCY_EXCHANGE_RATE", 
    "from_currency":"CAD",
    "to_currency":"USD"
    }

try:
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    json_response = response.json()['Realtime Currency Exchange Rate']

    _from = f"1 {str(json_response['2. From_Currency Name'])} ({str(json_response['1. From_Currency Code'])})  equals "
    _to = f"{str(json_response['4. To_Currency Name'])} ({str(json_response['3. To_Currency Code'])})"
    _rate = str(json_response['5. Exchange Rate'])
    _datetime = f"Last Updated: {str(json_response['6. Last Refreshed'])} Timezone: {str(json_response['7. Time Zone'])}"
except:
    _from = "Error"
    _to, _rate, _datetime = "", "", ""

'''
for key, value in json_response.items():
    print(f"{key[3:]}: {value}")
'''

@app.route('/')
def home():
    return render_template('index.html')
    #return render_template('index.html', _to=_to, _from=_from, _rate=_rate, _datetime=_datetime)

if __name__ == "__main__":
	app.run(debug=True)