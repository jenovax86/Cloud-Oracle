import sqlite3

sqlite_connection = sqlite3.connect("weather_forecast")
cursor = sqlite_connection.cursor()
query = """
            CREATE TABLE IF NOT EXISTS weather(
            id INTEGER PRIMARY KEY NOT NULL,
            date TEXT NOT NULL,
            low_temperature TEXT NOT NULL,
            high_temperature TEXT NOT NULL
            )
            """
cursor.execute(query)
sqlite_connection.commit()
cursor.close()
