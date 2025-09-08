import pandas as pd
import sqlite3
from crawler import scrape_weather_data


def connect():
    con = sqlite3.connect("weather_forecast")
    return con


def create_table(connection):
    cursor = connection.cursor()
    query = """
            CREATE TABLE IF NOT EXISTS weather_data(
                id INTEGER PRIMARY KEY,
                month TEXT NOT NULL,
                day TEXT NOT NULL,
                date TEXT NOT NULL,
                lowest_temperature INTEGER NOT NULL,
                highest_temperature INTEGER NOT NULL
            )
            """
    cursor.execute(query)
    cursor.close()

def insert_weather_records(connection, weather_records):
    cursor = connection.cursor()
    query = """
            INSERT OR REPLACE INTO weather_data(month, day, date, lowest_temperature, highest_temperature) VALUES (?, ?, ?, ?, ?);
        """

    for row in weather_records.itertuples():
        cursor.execute(
            query,
            (
                str(row.month),
                str(row.day),
                str(row.date),
                float(row.lowest_temperature),
                float(row.highest_temperature),
            ),
        )
    connection.commit()
    cursor.close()


def get_weather_records(connection):
    cursor = connection.cursor()
    query = """
            SELECT id, month, day, date, lowest_temperature, highest_temperature FROM weather_data ORDER BY date;
            """
    result = cursor.execute(query)
    records = result.fetchall()
    return pd.DataFrame(records)
