from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

#load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.rout('/weather', methods=['POST'])
def get_weather():


    return 