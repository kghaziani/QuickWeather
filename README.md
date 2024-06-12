# QuickWeather
## Video Demo:  <URL HERE>
## Description:
QuickWeather gives people quick and simple access to weather information. Users can enter a location and get today’s weather, an hourly weather chart, and a weather forecast. Current temperature, weather condition, wind condition, and humidity.

QuickWeather was created using HTML CSS, Flask, Javascript, and a weather API(https://www.weatherapi.com/).

Design
My goal was to ensure that users would not need to scroll to get what they need. All information should be readily available for utility.

## app.py

I used flask to host QuickWeather and [app.py](http://app.py) stores the code. 

app.py imports flask, requests for the API call, dotenv so I can secure my API key, and datetime to alter time data.  I used a .env file to secure the API key, used the load_dotenv() to load my API key, then stored with the variable with os.getenv() into a API_KEY. 

```python
app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")
```

The proceeding implementation in [app.py](http://app.py) uses two routes: ‘/’, and ‘/weather’, whose method is POST. I use request.form.get() to capture the location and store it in location_query. I use two separate variables to capture API responses for the current weather and the forecast weather:

```python
# Request current weather and 7-day forecast
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location_query}&aqi=yes"
    url2 = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location_query}&days=7&aqi=yes&alerts=no"
    response = requests.get(url)
    response2 = requests.get(url2)
```

I create variables for the necessary data that will be passed as arguments and returned to weather.html.

I wanted to change the format of the API response’s time data so I created new variables to get the name of the day and AM/PM:

```python
# Convert date to day name
        for day in forecast:
            day_date = datetime.strptime(day['date'], '%Y-%m-%d')
            day['day_name'] = day_date.strftime('%A')

        # Get current time
        current_time = datetime.now()
        end_time = current_time + timedelta(hours=24)

        # Convert localtime to show just time and day
        localtime = datetime.strptime(location['localtime'], '%Y-%m-%d %H:%M')
        formatted_localtime = localtime.strftime('%A, %I:%M %p')
```

I had to create a for loop so I can show also show hourly data.

## Templates:

## index.html:

I went for simple design aesthetics for the web page. The background is light orange cream color representing summer weather vibes. Index.html holds the layout of the page and uses bootstrap for styling. There is a navbar at the top for aesthetic purposes with a sun icon. The form asks the user for a location with a submit button on the left. Underneath there is a tagline text. I ensured that these elements were centered and the top of the page and ready for user access.

## weather.html:

The page has three components: current weather card, 24-hour weather chart, and weekly weather. I made the current weather elements side-by-side using a flex container. The current weather is represented as a card with time, temperature, weather condition, wind, and humidity information. 

I used javascript to create the chart. This was done by parsing data using jinga to convert data from our flask app into JSON format and creating a Chart. 

The weekly weather forecast uses Tailwind styling to create a grid with 7 columns and outputs the 7-day weather data using a for loop.


## style.css:

I used flex containers and flex child for organizing current weather contents.

```css
.flex-container {
    display: flex;
    margin: 20px;
}

.flex-child {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}  

.flex-child:first-child {
    margin-right: 20px;
} 
```

I needed to style the current weather card differently than the forecast card because its size needed to be adjusted to correspond with the chart. I created a new style called card-main for this task:

```
.card-main {
    width: 300px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: row;
    overflow: hidden;
}
```