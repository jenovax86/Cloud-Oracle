import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

WEATHER_DATA = pd.read_csv("../data/weather_data.csv")

try:
    my_db = mysql.connector.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)


def insert_record(connection, weather_records):
    cursor = connection.cursor()
    query = """
                INSERT INTO weather_data(month, day, date, lowest_temperature, highest_temperature) VALUES(%s, %s, %s, %s, %s);
             """

    for row in weather_records.itertuples(index=False):
        cursor.execute(
            query,
            (
                row.month,
                row.day,
                row.date,
                int(row.lowest_temperature),
                int(row.highest_temperature),
            ),
        )

    result = cursor.fetchall()
    cursor.close()
    return result


def retrieve_data(connection):
    cursor = connection.cursor()

    retrieve_data_query = """
            SELECT month, day, date, lowest_temperature, highest_temperature FROM weather_data ORDER BY date;
            """

    cursor.execute(retrieve_data_query)
    result = cursor.fetchall()
    cursor.close()
    return result


if my_db.is_connected():
    insert_data = insert_record(my_db, WEATHER_DATA)
    get_data = retrieve_data(my_db)
    print(get_data)
    my_db.close()
