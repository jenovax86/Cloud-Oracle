import pandas as pd
from utils import get_year_from_date


def find_min_and_max_year(connection):
    cursor = connection.cursor()
    query = """
            SELECT MAX(date), MIN(date) FROM weather;
            """
    result = cursor.execute(query).fetchall()
    max_year = None if result[0][0] is None else get_year_from_date(result[0][0])
    min_year = None if result[0][1] is None else get_year_from_date(result[0][1])
    return max_year, min_year


def insert_weather_records(connection, weather_records):
    cursor = connection.cursor()
    query = """
                INSERT OR IGNORE INTO weather(date, low_temperature, high_temperature) VALUES(?, ?, ?)
                """
    for record in weather_records:
        cursor.execute(
            query,
            (record["date"], record["low_temperature"], record["high_temperature"]),
        )
    connection.commit()


def get_weather_records(connection):
    cursor = connection.cursor()
    query = """
            SELECT id, date, low_temperature, high_temperature FROM weather ORDER BY date;
            """
    result = cursor.execute(query).fetchall()
    return result
