import pandas as pd
from database.migration_v1 import CONNECTION


def find_last_year():
    cursor = CONNECTION.cursor()
    query = """
            SELECT MAX(date) FROM weather ORDER BY date;
            """
    result = cursor.execute(query)
    records = result.fetchall()
    return records[0][0]


def insert_weather_records(weather_records):
    cursor = CONNECTION.cursor()

    query = """
                INSERT OR IGNORE INTO weather(date, low_temperature, high_temperature) VALUES(?, ?, ?)
                """
    for record in weather_records:
        cursor.execute(
            query,
            (record["date"], record["low_temperature"], record["high_temperature"]),
        )
    cursor.fetchall()
    CONNECTION.commit()


def get_weather_records():
    cursor = CONNECTION.cursor()
    query = """
            SELECT id, date, low_temperature, high_temperature FROM weather ORDER BY date;
            """
    result = cursor.execute(query)
    records = result.fetchall()
    return pd.DataFrame(records)
