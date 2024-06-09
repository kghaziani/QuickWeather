from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    location_query = request.form.get('location')
    if not location_query:
        return "Please enter a valid location"

    # Request current weather and 7-day forecast
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location_query}&aqi=yes"
    url2 = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location_query}&days=7&aqi=yes&alerts=no"
    response = requests.get(url)
    response2 = requests.get(url2)

    if response.status_code != 200 or response2.status_code != 200:
        return "Sorry, couldn't fetch the weather data"

    data = response.json()
    data2 = response2.json()

    try:
        location = data['location']
        current_temp = data['current']['temp_f']
        current_condition = data['current']['condition']['text']
        condition_icon = data['current']['condition']['icon']
        forecast = data2['forecast']['forecastday']

        # Convert date to day name
        for day in forecast:
            day_date = datetime.strptime(day['date'], '%Y-%m-%d')
            day['day_name'] = day_date.strftime('%A')

        # Get current time
        current_time = datetime.now()
        end_time = current_time + timedelta(hours=24)

        # Filter hourly data for the next 24 hours
        hourly_forecast = []
        hours = []
        temperatures = []
        for day in forecast:
            for hour in day['hour']:
                hour_time = datetime.strptime(hour['time'], '%Y-%m-%d %H:%M')
                if current_time <= hour_time < end_time:
                    hourly_forecast.append(hour)
                    hours.append(hour_time.strftime('%I %p'))  # Format time as HH AM/PM
                    temperatures.append(hour['temp_f'])

    except KeyError as e:
        return f"Missing key in the API response: {e}"

    return render_template('weather.html', location=location, temp=current_temp, condition=current_condition, condition_icon=condition_icon, forecast=forecast, hourly_forecast=hourly_forecast, hours=hours, temperatures=temperatures)

if __name__ == '__main__':
    app.run(debug=True)
