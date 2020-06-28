import io
import requests
from flask import Response
from flask import Flask, redirect, url_for, render_template
from config import headers

app = Flask(__name__)

url = "https://alpha-vantage.p.rapidapi.com/query"

if __name__ == "__main__":
	app.run(debug=True)