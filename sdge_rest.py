from flask import Flask, jsonify 

import os
import time
from xml.dom.minidom import parse

import datastore 

app = Flask(__name__)
app.debug = True
app.store = datastore.DataStore()
app.store.load("sdge.xml")

@app.route('/api/1.0/year/<int:year>/')
def year_data(year): 
    data = app.store.get_year(year) 
    return jsonify(data)

@app.route('/api/1.0/year/<int:year>/month/<int:month>')
def year_month_data(year, month): 
    data = app.store.get_month(year, month) 
    return jsonify(data)

@app.route('/api/1.0/year/<int:year>/week/<int:week>')
def year_week_data(year, week): 
    data = app.store.get_week(year, week) 
    return jsonify(data)

@app.route('/api/1.0/year/<int:year>/day/<int:day>')
def year_day_data(year, day): 
    data = app.store.get_day(year, day) 
    return jsonify(data)

@app.route('/')
def hello_world():
    return "Hello" 

if __name__ == '__main__':
    app.run()
