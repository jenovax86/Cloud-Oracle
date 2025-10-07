import sqlite3
import constants
from crawler import scrape_weather_data
from database.db import find_min_and_max_year

def main():
    sqlite_connection = sqlite3.connect("weather_forecast")
    try:
        max_year, min_year = find_min_and_max_year(sqlite_connection)
        if max_year is None:
            return scrape_weather_data(sqlite_connection, constants.PAST_YEAR, constants.LAST_AVAILABLE_YEAR)
        if constants.PAST_YEAR > max_year:
            return scrape_weather_data(sqlite_connection, constants.PAST_YEAR, max_year)
        if min_year != constants.LAST_AVAILABLE_YEAR:
            return scrape_weather_data(sqlite_connection, min_year - 1, constants.LAST_AVAILABLE_YEAR)
    finally:
        sqlite_connection.close()


if __name__ == "__main__":
    main()
