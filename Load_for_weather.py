import psycopg2

def load_to_postgres(weather_data):
    conn = psycopg2.connect(
        host="localhost",
        database="weatherdb",
        user="postgres",
        password="your_password"
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
        weather_data["city"],
        weather_data["country"],
        weather_data["description"],
        weather_data["temperature"],
        weather_data["humidity"],
        weather_data["wind_speed"],
        weather_data["timestamp"]
    ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded into PostgreSQL.")
