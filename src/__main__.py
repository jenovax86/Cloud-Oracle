from crawler import scrape_weather_data
from db import connect, create_table, insert_weather_records, get_weather_records
import pandas as pd

def process_weather_database(records):
    connection = connect()
    create_table(connection)
    insert_weather_records(connection, records)
    get_all_records = get_weather_records(connection)
    return pd.DataFrame(get_all_records)


def main():
    weather_records = scrape_weather_data()
    database = process_weather_database(weather_records)
    print(database)
    


if __name__ == "__main__":
    main()