import requests
import psycopg2
import json
import os
from datetime import datetime

# Step 1: Extract weather data from OpenWeatherMap API
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
        print("API Error:", response.json())
        return None

# Step 2: Load data into PostgreSQL
def load_to_postgres(data):
    conn = psycopg2.connect(
        host="localhost",
        database="weatherdb",
        user="postgres",
        password="root"  # ⬅️ Replace this with your actual PostgreSQL password
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id SERIAL PRIMARY KEY,
            city VARCHAR(50),
            country VARCHAR(10),
            description TEXT,
            temperature REAL,
            humidity INT,
            wind_speed REAL,
            timestamp TIMESTAMP
        );
    """)

    cursor.execute("""
        INSERT INTO weather (city, country, description, temperature, humidity, wind_speed, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (
        data["city"],
        data["country"],
        data["description"],
        data["temperature"],
        data["humidity"],
        data["wind_speed"],
        data["timestamp"]
    ))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data inserted into PostgreSQL.")

# Step 3: Save a local backup JSON file
def save_local_backup(data, folder="daily_backups"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Convert datetime to string
    data["timestamp"] = data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    filename = f"{folder}/{data['city']}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Saved local backup: {filename}")


# Run the ETL pipeline
if __name__ == "__main__":
    city = input("Enter city: ")
    data = extract_weather(city)
    if data:
        load_to_postgres(data)
        save_local_backup(data)

