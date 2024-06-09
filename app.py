from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

#load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    #get location
    location =request.form.get('location')
    #handle if no location is incorrect
    if not location:
        return "please enter valid location"
    #make api request
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=yes"
    url2 = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=7&aqi=yes"
    response= requests.get(url)
    response2= requests.get(url2)

    #check if api request was successful
    if response.status_code !=200 or response2.status_code != 200:
        return "sorry, couldn't get weather data"

    data = response.json()
    data2 = response2.json()
    print(data2)
    

    try:
        location = data['location']
        current_temp = data['current']['temp_f']
        current_condition= data['current']['condition']['text']
        current_condition_icon= data['current']['condition']['icon']
        forecast = data2['forecast']['forecastday']

    except KeyError as e:
        return f"Missing key in the api response "
  
    return render_template('weather.html',
                           location=location, temp = current_temp, condition=current_condition, condition_icon=current_condition_icon,
                           forecast=forecast)
if __name__ == '__main__':
    app.run(debug=True)