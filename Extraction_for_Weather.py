import requests
from datetime import datetime

def extract_weather(city):
    API_KEY = "d954519d1325150c26a422c548c9ab34"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now()
        }
    else:
        print("Error:", response.json())
        return None
