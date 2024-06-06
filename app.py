from flask import Flask, render_template, request
import requests


app = Flask(__name__)
API_KEY = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.rout('/weather', methods=['POST'])
def get_weather():


    return 