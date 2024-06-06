from flask import Flask, render_template, request
import requests


app = Flask(__name__)
API_KEY = 'd1baf78743988d70f1b075cd6a3d1dd1'

@app.route('/')
def index():
    return render_template('index.html')

@app.rout('/weather', methods=['POST'])
def get_weather():
    

    return 