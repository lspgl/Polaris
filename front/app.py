from flask import Flask, render_template, jsonify
import datetime
import sys
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(__location__ + '/../')

from core.transportData import SbbProvider, get_departures

app = Flask(__name__,
            static_url_path='/static')

templates = {'index': 'index.html', }

provider = SbbProvider(n_req=20)


@app.route('/')
def index():
    return render_template(templates['index'])


@app.route('/get_departures_req')
def get_departures_req():
    data = get_departures(provider)

    return jsonify(data)
