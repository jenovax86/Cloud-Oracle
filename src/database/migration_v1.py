import sqlite3

CONNECTION = sqlite3.connect("weather_forecast")


def create_table():

    cursor = CONNECTION.cursor()
    query = """
            CREATE TABLE IF NOT EXISTS weather(
            id INTEGER PRIMARY KEY NOT NULL,
            date TEXT UNIQUE NOT NULL,
            low_temperature TEXT NOT NULL,
            high_temperature TEXT NOT NULL
            )
            """
    cursor.execute(query)
    CONNECTION.commit()
    cursor.close()


create_table()
